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

# --- Tinker Client ---
# Initialize Tinker Client
# Note: In production, ensure TINKER_API_KEY is set
tinker_api_key = os.environ.get("TINKER_API_KEY")
if not tinker_api_key:
    print("Warning: TINKER_API_KEY not set.")

# --- Models ---
class ChatRequest(BaseModel):
    user_id: str
    message: str

class ChatResponse(BaseModel):
    response: str
    mood: str

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
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO relationships (user_id, affinity, interaction_count, last_interaction)
            VALUES (%s, %s, 1, CURRENT_TIMESTAMP)
            ON CONFLICT (user_id) DO UPDATE 
            SET affinity = relationships.affinity + %s,
                interaction_count = relationships.interaction_count + 1,
                last_interaction = CURRENT_TIMESTAMP
            RETURNING affinity
        """, (user_id, affinity_change, affinity_change))
        conn.commit()
        return cur.fetchone()[0]

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
        # Default: +0.1 affinity per interaction
        affinity = update_relationship(conn, request.user_id, affinity_change=0.1)
        
        if affinity < -5.0:
            return ChatResponse(response="I don't want to talk to you.", mood="hostile")

        # 3. Construct Prompt (Placeholder for now)
        # In Phase 4, we will inject relationship state and internal monologue here.
        prompt = request.message

        # 3. Call Tinker (Mock for now, until API is fully integrated)
        # TODO: Replace with actual Tinker call using the trained adapter
        # response_text = tinker_client.generate(prompt, adapter="generic-human-v2")
        
        # Mock response for testing deployment
        mock_responses = [
            "I'm listening.", 
            "That's interesting.", 
            "Why do you say that?", 
            "I'm a bit tired, but go on."
        ]
        response_text = random.choice(mock_responses)

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
