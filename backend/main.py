from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import os
import tinker
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List, Optional
import random
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# --- Database Connection ---
def get_db_connection():
    conn = psycopg2.connect(os.environ["DATABASE_URL"])
    return conn

# --- Tinker Client Setup ---
tinker_api_key = os.environ.get("TINKER_API_KEY")
service_client = None
sampling_client = None
tokenizer = None

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
        checkpoints = rest_client.list_user_checkpoints().result()
        
        # Filter for our model
        target_cp = None
        for cp in checkpoints:
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

        # 2. Check/Update Relationship
        affinity = update_relationship(conn, request.user_id, affinity_change=0.1)
        
        if affinity < -5.0:
            return ChatResponse(response="I don't want to talk to you.", mood="hostile")

        # 3. Generate Response via Tinker
        response_text = ""
        if sampling_client and tokenizer:
            try:
                # Construct Prompt
                # TODO: Inject internal state based on bio_state/affinity if needed
                # For now, just pass the user message as raw text (DailyDialog style)
                prompt_text = request.message
                
                # Tokenize
                tokens = tokenizer.encode(prompt_text)
                model_input = tinker.types.ModelInput.from_ints(tokens)
                
                # Sample
                sampling_params = tinker.types.SamplingParams(max_tokens=150, temperature=0.8)
                future = sampling_client.sample(prompt=model_input, num_samples=1, sampling_params=sampling_params)
                result = future.result()
                
                # Decode
                if result.sequences:
                    # result.sequences[0] is a SampledSequence, which has .tokens
                    generated_tokens = result.sequences[0].tokens
                    response_text = tokenizer.decode(generated_tokens)
                else:
                    response_text = "..."
            except Exception as e:
                print(f"Tinker generation failed: {e}")
                response_text = "[Brain Error]"
        else:
            # Fallback if Tinker not connected
            response_text = "[Tinker not connected. Check logs.]"

        # 4. Update State
        new_adenosine = update_biological_state(conn)
        
        # 5. Log Chat
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
