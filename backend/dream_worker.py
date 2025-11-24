import os
import json
import psycopg2
from psycopg2.extras import RealDictCursor
import tinker
from tinker import types
from dotenv import load_dotenv
import datetime

# Load environment variables
load_dotenv("backend/.env")

DATABASE_URL = os.getenv("DATABASE_URL")
TINKER_API_KEY = os.getenv("TINKER_API_KEY")

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

def fetch_memories(conn):
    """Fetch chat logs from the last 24 hours (or all un-processed)."""
    # For simplicity, we'll just fetch the last 100 interactions
    # In a real system, we'd track which logs have been "dreamt" about.
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("""
            SELECT user_id, message, response 
            FROM chat_logs 
            ORDER BY timestamp DESC 
            LIMIT 100
        """)
        return cur.fetchall()

def format_data_for_training(memories):
    """Convert chat logs into Tinker Datum objects."""
    data = []
    for mem in memories:
        # We want to reinforce the AI's responses
        # Format: User: <msg> \n Caz: <response>
        # This matches the DailyDialog format we likely used (or close to it)
        # Wait, prepare_data.py used: {"prompt": msg1, "completion": msg2}
        # And upload_and_train.py used: text = f"{prompt} {completion}"
        
        # Let's try to match the format used in training.
        # In train_organism.py, we constructed Datum from text.
        # We need to know the exact format. 
        # prepare_data.py produced JSONL with "prompt" and "completion".
        # train_organism.py loaded that.
        
        # Let's assume the model expects: "User: <msg>\nCaz: <response>" if that's what we trained on.
        # Actually, looking at prepare_data.py, it just dumped raw text from DailyDialog?
        # "prompt": msg1['value'], "completion": msg2['value']
        # It didn't add "User:" or "Caz:".
        # BUT, the `generate_advanced_data.py` used raw text too.
        
        # However, for the *chat* interface, we usually want some delimiters.
        # In `main.py`, I tokenized `request.message` directly as the prompt.
        # So the model is acting as a completion engine.
        # If I train on "User: ...", I need to make sure inference uses "User: ...".
        # Currently `main.py` sends raw message.
        # If the model was trained on DailyDialog (which is just raw turns), it might be fine.
        
        # Let's stick to the raw format for now to match Phase 2.
        # Prompt: User Message
        # Target: AI Response
        
        # We need to tokenize this.
        # We'll need the tokenizer from the client.
        pass 
    return data

def dream_cycle():
    print("Starting Dream Cycle...")
    
    if not TINKER_API_KEY:
        print("Error: TINKER_API_KEY not found.")
        return

    # 1. Initialize Database
    conn = get_db_connection()
    
    # 2. Fetch Memories
    print("Fetching memories...")
    memories = fetch_memories(conn)
    if not memories:
        print("No memories found. Sleeping without dreaming.")
        conn.close()
        return
    
    print(f"Found {len(memories)} memories.")

    # 3. Initialize Tinker
    print("Initializing Tinker...")
    service_client = tinker.ServiceClient(api_key=TINKER_API_KEY)
    
    # Create Training Client to get tokenizer and load state
    # We need to resume from "generic-human-v2-state"
    # But first we need a client. We can create a LoRA client on the base model, 
    # then load the state.
    training_client = service_client.create_lora_training_client(base_model="meta-llama/Llama-3.1-8B")
    tokenizer = training_client.get_tokenizer()
    
    # 4. Prepare Data
    print("Preparing training data...")
    training_data = []
    for mem in memories:
        # Simple format: Prompt + Response
        # We need to encode it.
        # train_organism.py logic:
        # input_ids = tokenizer.encode(text)
        # target_ids = input_ids[:] (for causal LM)
        # But we want to mask the prompt? 
        # For simplicity, let's just train on the whole sequence for now (User + AI).
        # Or better: Prompt = User, Target = AI.
        
        # Let's construct the full text
        full_text = f"{mem['message']} {mem['response']}"
        encoded = tokenizer.encode(full_text)
        
        # Create Datum
        # We need to match the input expected by the model.
        # In train_organism.py, we used:
        # inputs = tinker.TensorData(data=encoded, shape=[len(encoded)])
        # targets = tinker.TensorData(data=encoded, shape=[len(encoded)])
        # datum = tinker.Datum(inputs={"input_ids": inputs, "labels": targets})
        
        # Create ModelInput
        chunk = tinker.EncodedTextChunk(tokens=encoded)
        model_input = tinker.ModelInput(chunks=[chunk])
        
        # Create Labels & Weights
        labels_tensor = tinker.TensorData(data=encoded, dtype="int64", shape=[len(encoded)])
        weights_data = [1.0] * len(encoded)
        weights_tensor = tinker.TensorData(data=weights_data, dtype="float32", shape=[len(encoded)])
        
        datum = tinker.Datum(
            model_input=model_input,
            loss_fn_inputs={
                "target_tokens": labels_tensor,
                "weights": weights_tensor
            }
        )
        training_data.append(datum)

    # 5. Load State
    print("Loading biological state (model weights)...")
    try:
        # Find latest state checkpoint
        rest_client = service_client.create_rest_client()
        checkpoints_response = rest_client.list_user_checkpoints().result()
        
        target_state_cp = None
        for cp in checkpoints_response.checkpoints:
            # We look for 'training' type checkpoint with our name
            if "generic-human-v2-state" in cp.checkpoint_id and cp.checkpoint_type == "training":
                target_state_cp = cp
                break
        
        if target_state_cp:
            print(f"Found state: {target_state_cp.tinker_path}")
            training_client.load_state(target_state_cp.tinker_path).result()
            print("State loaded.")
        else:
            print("Warning: No state found. Starting fresh.")

    except Exception as e:
        print(f"Error loading state: {e}")
        print("Starting fresh...")
    
    # 6. Dreaming (Fine-tuning)
    print("Dreaming (Fine-tuning)...")
    # Run a few steps
    # We'll just do one pass over the data (1 epoch)
    batch_size = 4
    for i in range(0, len(training_data), batch_size):
        batch = training_data[i:i+batch_size]
        
        # Forward/Backward
        loss = training_client.forward_backward(batch, loss_fn="cross_entropy").result()
        print(f"Batch {i//batch_size}: Loss = {loss}")
        
        # Optimizer Step
        training_client.optim_step(tinker.types.AdamParams(learning_rate=1e-5)).result()
        
    print("Dreaming complete.")

    # 7. Save New State
    print("Saving new biological state...")
    # Overwrite the state so we can resume next time
    training_client.save_state("generic-human-v2-state").result()
    
    # 8. Save Inference Weights
    print("Updating personality (inference weights)...")
    # This will create a new checkpoint for the backend to pick up
    training_client.save_weights_for_sampler("generic-human-v2").result()

    # 9. Reset Biological Markers
    print("Waking up... Resetting adenosine.")
    with conn.cursor() as cur:
        cur.execute("UPDATE biological_state SET adenosine = 0.0, sleep_mode = FALSE, last_updated = CURRENT_TIMESTAMP")
        conn.commit()
    
    conn.close()
    print("Dream Cycle Complete. Organism is awake and evolved.")

if __name__ == "__main__":
    dream_cycle()
