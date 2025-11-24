from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import os
import tinker
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List, Optional
import random

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

        # 2. Construct Prompt (Placeholder for now)
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
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO chat_logs (user_id, message, response, biological_state_snapshot)
                VALUES (%s, %s, %s, %s)
            """, (request.user_id, request.message, response_text, json.dumps(bio_state)))
            conn.commit()

        return ChatResponse(response=response_text, mood="awake")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

import json
