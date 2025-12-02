import os
import json
import psycopg2
from psycopg2.extras import RealDictCursor
import tinker
from tinker import types
from dotenv import load_dotenv
import logging
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Brain:
    def __init__(self):
        load_dotenv()
        self.db_url = os.environ.get("DATABASE_URL")
        self.tinker_api_key = os.environ.get("TINKER_API_KEY")
        
        self.service_client = None
        self.sampling_client = None
        self.tokenizer = None
        
        self._initialize_tinker()
        self._initialize_db()

    def _initialize_db(self):
        """Initialize database connection and ensure tables exist."""
        try:
            conn = self.get_db_connection()
            with conn.cursor() as cur:
                # Ensure biological_state exists
                cur.execute("CREATE TABLE IF NOT EXISTS biological_state (adenosine FLOAT, sleep_mode BOOLEAN, last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
                # Ensure relationships exists
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS relationships (
                        user_id TEXT PRIMARY KEY, 
                        affinity FLOAT, 
                        interaction_count INT, 
                        last_interaction TIMESTAMP,
                        name TEXT,
                        secret_phrase TEXT
                    )
                """)
                # Ensure chat_logs exists
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS chat_logs (
                        id SERIAL PRIMARY KEY,
                        user_id TEXT,
                        message TEXT,
                        response TEXT,
                        biological_state_snapshot JSONB,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Initialize bio state if empty
                cur.execute("SELECT COUNT(*) FROM biological_state")
                if cur.fetchone()[0] == 0:
                    cur.execute("INSERT INTO biological_state (adenosine, sleep_mode) VALUES (0.0, FALSE)")
                
                conn.commit()
            conn.close()
            logger.info("Database initialized.")
        except Exception as e:
            logger.error(f"Database initialization failed: {e}")

    def _initialize_tinker(self):
        """Initialize Tinker clients."""
        if self.tinker_api_key:
            try:
                logger.info("Initializing Tinker Clients...")
                self.service_client = tinker.ServiceClient(api_key=self.tinker_api_key)
                
                # 1. Get Tokenizer
                training_client = self.service_client.create_lora_training_client(base_model="meta-llama/Llama-3.1-8B")
                self.tokenizer = training_client.get_tokenizer()
                
                # 2. Find latest generic-human-v2 checkpoint
                rest_client = self.service_client.create_rest_client()
                checkpoints_response = rest_client.list_user_checkpoints().result()
                
                target_cp = None
                for cp in checkpoints_response.checkpoints:
                    if "generic-human-v2" in cp.checkpoint_id and cp.checkpoint_type == "sampler":
                        target_cp = cp
                        break 
                
                if target_cp:
                    logger.info(f"Found checkpoint: {target_cp.tinker_path}")
                    self.sampling_client = self.service_client.create_sampling_client(model_path=target_cp.tinker_path)
                else:
                    logger.warning("No 'generic-human-v2' checkpoint found. Chat will fail.")
                    
            except Exception as e:
                logger.error(f"Error initializing Tinker: {e}")
        else:
            logger.warning("TINKER_API_KEY not set.")

    def get_db_connection(self):
        return psycopg2.connect(self.db_url)

    def get_biological_state(self, conn):
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM biological_state LIMIT 1")
            return cur.fetchone()

    def update_biological_state(self, conn, adenosine_change=0.05):
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE biological_state 
                SET adenosine = LEAST(adenosine + %s, 1.0),
                    last_updated = CURRENT_TIMESTAMP
                RETURNING adenosine
            """, (adenosine_change,))
            conn.commit()
            return cur.fetchone()[0]

    def update_relationship(self, conn, user_id, affinity_change=0.0):
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

    def handle_auth_commands(self, conn, user_id, message):
        """Parse message for auth commands and update DB."""
        response_override = None
        
        # 1. Set Name: "My name is [Name]"
        name_match = re.search(r"my name is\s+([a-zA-Z]+)", message, re.IGNORECASE)
        if name_match:
            new_name = name_match.group(1)
            with conn.cursor() as cur:
                cur.execute("UPDATE relationships SET name = %s WHERE user_id = %s", (new_name, user_id))
                conn.commit()
            
        # 2. Set Secret: "Set secret [Secret]"
        secret_match = re.search(r"set secret\s+(.+)", message, re.IGNORECASE)
        if secret_match:
            new_secret = secret_match.group(1).strip()
            with conn.cursor() as cur:
                cur.execute("UPDATE relationships SET secret_phrase = %s WHERE user_id = %s", (new_secret, user_id))
                conn.commit()
            response_override = "Secret set. I'll remember that."

        return response_override

    def generate_tinker_response(self, user_name, message):
        if not self.sampling_client or not self.tokenizer:
            return "[Brain not fully connected]"

        try:
            identity_label = f"User ({user_name})" if user_name else "User (Stranger)"
            prompt_text = f"{identity_label}: {message}\nCaz:"
            
            tokens = self.tokenizer.encode(prompt_text)
            model_input = tinker.types.ModelInput.from_ints(tokens)
            
            sampling_params = tinker.types.SamplingParams(
                max_tokens=150, 
                temperature=0.8, 
                stop_token_ids=[self.tokenizer.encode("\n")[0]]
            )
            
            future = self.sampling_client.sample(prompt=model_input, num_samples=1, sampling_params=sampling_params)
            result = future.result()
            
            if result.sequences:
                generated_tokens = result.sequences[0].tokens
                response_text = self.tokenizer.decode(generated_tokens)
                return response_text.replace("Caz:", "").strip()
            else:
                return "..."
        except Exception as e:
            logger.error(f"Tinker generation failed: {e}")
            return "[Brain Error]"

    def process_message(self, user_id: str, message: str):
        """Main entry point for processing a message."""
        conn = self.get_db_connection()
        try:
            # 1. Check Biological State
            bio_state = self.get_biological_state(conn)
            if bio_state["sleep_mode"] or bio_state["adenosine"] > 0.9:
                return {"response": "Zzz... (The organism is sleeping)", "mood": "asleep"}

            # 2. Update Relationship
            rel = self.update_relationship(conn, user_id, affinity_change=0.1)
            affinity = rel['affinity']
            user_name = rel['name']
            
            if affinity < -5.0:
                return {"response": "I don't want to talk to you.", "mood": "hostile"}

            # 3. Handle Auth Commands
            auth_response = self.handle_auth_commands(conn, user_id, message)
            if auth_response:
                return {"response": auth_response, "mood": "neutral"}

            # 4. Generate Response
            response_text = self.generate_tinker_response(user_name, message)

            # 5. Update State
            self.update_biological_state(conn)
            
            # 6. Log Chat
            bio_state_dict = dict(bio_state)
            if 'last_updated' in bio_state_dict:
                bio_state_dict['last_updated'] = str(bio_state_dict['last_updated'])

            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO chat_logs (user_id, message, response, biological_state_snapshot)
                    VALUES (%s, %s, %s, %s)
                """, (user_id, message, response_text, json.dumps(bio_state_dict)))
                conn.commit()

            return {"response": response_text, "mood": "awake"}

        finally:
            conn.close()

    async def process_message_async(self, user_id: str, message: str):
        """Async wrapper for process_message."""
        # Since DB and Tinker are sync, we might want to run this in a threadpool if it blocks too much.
        # For now, simple direct call is fine for low load.
        return self.process_message(user_id, message)

    def status(self):
        return {"status": "alive", "tinker_connected": self.sampling_client is not None}
