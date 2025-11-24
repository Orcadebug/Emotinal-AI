import os
import json
import tinker
from tinker import ServiceClient, Datum, ModelInput, EncodedTextChunk, TensorData, AdamParams
from dotenv import load_dotenv

load_dotenv("backend/.env")

API_KEY = os.getenv("TINKER_API_KEY")
if not API_KEY:
    print("Error: TINKER_API_KEY not found.")
    exit(1)

# Set the API key for the library
os.environ["TINKER_API_KEY"] = API_KEY

def train():
    print("Initializing Tinker Service Client...")
    client = ServiceClient()
    
    print("Creating LoRA Training Client (Base: Llama-3-8B-Base)...")
    # Note: Assuming 'llama-3-8b-base' is a valid model ID in Tinker. 
    # If not, user might need to change it.
    training_client = client.create_lora_training_client(
        base_model="meta-llama/Llama-3.1-8B",
        rank=32,
        train_mlp=True,
        train_attn=True
    )
    
    print("Getting Tokenizer...")
    tokenizer = training_client.get_tokenizer()
    
    # Load Data
    data_path = "data/final_training_set.jsonl"
    print("Loading Data...")
    if not os.path.exists(data_path):
        print(f"Error: {data_path} not found.")
        return
    
    with open(data_path, 'r') as f:
        lines = f.readlines()

    # Check for checkpoint
    start_index = 0
    checkpoint_file = "training_progress_full_v2.json"
    if os.path.exists(checkpoint_file):
        try:
            with open(checkpoint_file, 'r') as f:
                ckpt = json.load(f)
                start_index = ckpt.get("processed_count", 0)
                print(f"Resuming from index {start_index}...")
        except:
            print("Error reading checkpoint, starting from 0.")

    print(f"Found {len(lines)} examples. Starting training loop from {start_index}...")
    
    # Training Loop
    batch_size = 4
    accumulated_data = []
    
    import time
    
    def retry_api_call(func, *args, **kwargs):
        max_retries = 5
        base_delay = 2
        for attempt in range(max_retries):
            try:
                return func(*args, **kwargs).result()
            except Exception as e:
                if attempt == max_retries - 1:
                    raise e
                print(f"API call failed: {e}. Retrying in {base_delay}s...")
                time.sleep(base_delay)
                base_delay *= 2

    for i, line in enumerate(lines):
        if i < start_index:
            continue

        entry = json.loads(line)
        prompt = entry.get("prompt", "")
        completion = entry.get("completion", "")
        full_text = f"{prompt} {completion}"
        
        # Tokenize
        tokens = tokenizer.encode(full_text)
        
        chunk = EncodedTextChunk(tokens=tokens)
        model_input = ModelInput(chunks=[chunk])
        
        # Labels & Weights
        labels_tensor = TensorData(data=tokens, dtype="int64", shape=[len(tokens)])
        weights_data = [1.0] * len(tokens)
        weights_tensor = TensorData(data=weights_data, dtype="float32", shape=[len(tokens)])
        
        datum = Datum(
            model_input=model_input,
            loss_fn_inputs={
                "target_tokens": labels_tensor,
                "weights": weights_tensor
            } 
        )
        
        accumulated_data.append(datum)
        
        if len(accumulated_data) >= batch_size:
            # Forward Backward
            retry_api_call(
                training_client.forward_backward,
                data=accumulated_data,
                loss_fn="cross_entropy"
            )
            
            # Optimizer Step
            retry_api_call(
                training_client.optim_step,
                adam_params=AdamParams(learning_rate=1e-4)
            )
            
            accumulated_data = []
            
            # Save checkpoint
            with open(checkpoint_file, 'w') as f:
                json.dump({"processed_count": i + 1}, f)
            
            if (i + 1) % 100 == 0:
                print(f"Processed {i + 1}/{len(lines)} examples...")

    print("Saving Full Training State (for future updates)...")
    training_client.save_state("generic-human-v2-state").result()
    
    print("Saving Adapter for Inference...")
    training_client.save_weights_for_sampler("generic-human-v2").result()
    
    print("Training Complete! State and Adapter saved.")
    
    # Cleanup checkpoint
    if os.path.exists(checkpoint_file):
        os.remove(checkpoint_file)

if __name__ == "__main__":
    try:
        train()
    except Exception as e:
        print(f"Training failed: {e}")
        import traceback
        traceback.print_exc()
