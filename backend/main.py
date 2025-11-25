from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import os
import tinker
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List, Optional
import random
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware # Added this import
import json # Added this import

load_dotenv()

from voice_router import router as voice_router

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(voice_router) # Added this line

# --- Database Connection ---
def get_db_connection():
    conn = psycopg2.connect(os.environ["DATABASE_URL"])
    return conn

# --- Tinker Client Setup ---
tinker_api_key = os.environ.get("TINKER_API_KEY")
service_client = None
sampling_client = None
tokenizer = None

# --- Models ---
class ChatRequest(BaseModel):
    user_id: str
    message: str

class ChatResponse(BaseModel):
    response: str
    mood: str

if tinker_api_key:
    try:
        print("Initializing Tinker Clients...")
        service_client = tinker.ServiceClient(api_key=tinker_api_key)
        
        # 1. Get Tokenizer (via TrainingClient)
        # Use base model to get tokenizer
        training_client = service_client.create_lora_training_client(base_model="meta-llama/Llama-3.1-8B")
        tokenizer = training_client.get_tokenizer()
        
        # 2. Find latest generic-human-v2 checkpoint
        rest_client = service_client.create_rest_client()
        checkpoints_response = rest_client.list_user_checkpoints().result()
        
        # Filter for our model
        target_cp = None
        # checkpoints_response.checkpoints is the list
        for cp in checkpoints_response.checkpoints:
            if "generic-human-v2" in cp.checkpoint_id and cp.checkpoint_type == "sampler":
                target_cp = cp
                break # Assuming list is sorted by time desc, or we just take first match
        
        if target_cp:
            print(f"Found checkpoint: {target_cp.tinker_path}")
            sampling_client = service_client.create_sampling_client(model_path=target_cp.tinker_path)
        else:
            print("Warning: No 'generic-human-v2' checkpoint found. Chat will fail.")
            
    except Exception as e:
        print(f"Error initializing Tinker: {e}")
else:
    print("Warning: TINKER_API_KEY not set.")

# --- Gatekeeper Logic ---
def get_biological_state(conn):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT * FROM biological_state LIMIT 1")
        return cur.fetchone()

def update_biological_state(conn, adenosine_change=0.05):
    with conn.cursor() as cur:
        cur.execute("""
            UPDATE biological_state 
            SET adenosine = LEAST(adenosine + %s, 1.0),
                last_updated = CURRENT_TIMESTAMP
            RETURNING adenosine
        """, (adenosine_change,))
        conn.commit()
        return cur.fetchone()[0]

def update_relationship(conn, user_id, affinity_change=0.0):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("""
            INSERT INTO relationships (user_id, affinity, interaction_count, last_interaction)
            VALUES (%s, %s, 1, CURRENT_TIMESTAMP)
            ON CONFLICT (user_id) DO UPDATE 
            SET affinity = relationships.affinity + %s,
                interaction_count = relationships.interaction_count + 1,
                last_interaction = CURRENT_TIMESTAMP
            RETURNING affinity, name, secret_phrase
        """, (user_id, affinity_change, affinity_change))
        conn.commit()
        return cur.fetchone()

def handle_auth_commands(conn, user_id, message):
    """Parse message for auth commands and update DB."""
    import re
    response_override = None
    
    # 1. Set Name: "My name is [Name]"
    name_match = re.search(r"my name is\s+([a-zA-Z]+)", message, re.IGNORECASE)
    if name_match:
        new_name = name_match.group(1)
        with conn.cursor() as cur:
            cur.execute("UPDATE relationships SET name = %s WHERE user_id = %s", (new_name, user_id))
            conn.commit()
        # We don't override response, we let the AI acknowledge it naturally, 
        # but we might inject a system note if we were using system prompts.
        # For now, the AI will just see "User (Name): My name is Name" next time.
        
    # 2. Set Secret: "Set secret [Secret]"
    secret_match = re.search(r"set secret\s+(.+)", message, re.IGNORECASE)
    if secret_match:
        new_secret = secret_match.group(1).strip()
        with conn.cursor() as cur:
            cur.execute("UPDATE relationships SET secret_phrase = %s WHERE user_id = %s", (new_secret, user_id))
            conn.commit()
        response_override = "Secret set. I'll remember that."

    return response_override

# --- Routes ---
@app.get("/")
def read_root():
    return {"status": "alive", "message": "The organism is breathing."}

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    conn = get_db_connection()
    try:
        # 1. Check Biological State (Sleep)
        bio_state = get_biological_state(conn)
        if not bio_state:
            # Initialize if empty
            with conn.cursor() as cur:
                cur.execute("INSERT INTO biological_state (adenosine, sleep_mode) VALUES (0.0, FALSE)")
                conn.commit()
            bio_state = {"adenosine": 0.0, "sleep_mode": False}

        if bio_state["sleep_mode"] or bio_state["adenosine"] > 0.9:
            return ChatResponse(response="Zzz... (The organism is sleeping)", mood="asleep")

        # 2. Check/Update Relationship & Auth
        rel = update_relationship(conn, request.user_id, affinity_change=0.1)
        affinity = rel['affinity']
        user_name = rel['name']
        
        if affinity < -5.0:
            return ChatResponse(response="I don't want to talk to you.", mood="hostile")

        # 3. Handle Auth Commands
        auth_response = handle_auth_commands(conn, request.user_id, request.message)
        if auth_response:
            return ChatResponse(response=auth_response, mood="neutral")

        # 4. Generate Response via Tinker
        response_text = ""
        if sampling_client and tokenizer:
            try:
                # Construct Prompt with Identity
                # If name is known, use it. Else "Stranger".
                identity_label = f"User ({user_name})" if user_name else "User (Stranger)"
                
                # We format it somewhat like a script to give the AI context
                # "User (Name): Message"
                prompt_text = f"{identity_label}: {request.message}\nCaz:"
                
                # Tokenize
                tokens = tokenizer.encode(prompt_text)
                model_input = tinker.types.ModelInput.from_ints(tokens)
                
                # Sample
                sampling_params = tinker.types.SamplingParams(max_tokens=150, temperature=0.8, stop_token_ids=[tokenizer.encode("\n")[0]]) 
                # Note: Stop at newline to prevent generating user's next turn if it tries to hallucinate it.
                # But we need to check what the newline token is. Usually 13 or similar.
                # Let's just try without explicit stop tokens first, or use a simple one.
                
                future = sampling_client.sample(prompt=model_input, num_samples=1, sampling_params=sampling_params)
                result = future.result()
                
                # Decode
                if result.sequences:
                    generated_tokens = result.sequences[0].tokens
                    response_text = tokenizer.decode(generated_tokens)
                    # Strip "Caz:" if it generated it (unlikely with our prompt structure but possible)
                    response_text = response_text.replace("Caz:", "").strip()
                else:
                    response_text = "..."
            except Exception as e:
                print(f"Tinker generation failed: {e}")
                response_text = "[Brain Error]"
        else:
            # Fallback if Tinker not connected
            response_text = "[Tinker not connected. Check logs.]"

        # 5. Update State
        new_adenosine = update_biological_state(conn)
        
        # 6. Log Chat
        # Convert RealDictRow to dict and handle datetime
        bio_state_dict = dict(bio_state)
        if 'last_updated' in bio_state_dict:
            bio_state_dict['last_updated'] = str(bio_state_dict['last_updated'])

        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO chat_logs (user_id, message, response, biological_state_snapshot)
                VALUES (%s, %s, %s, %s)
            """, (request.user_id, request.message, response_text, json.dumps(bio_state_dict)))
            conn.commit()

        return ChatResponse(response=response_text, mood="awake")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

import json
