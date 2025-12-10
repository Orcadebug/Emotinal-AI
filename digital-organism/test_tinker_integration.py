import os
import tinker
from tinker import types
from dotenv import load_dotenv

load_dotenv("backend/.env")

def test_tinker():
    api_key = os.getenv("TINKER_API_KEY")
    if not api_key:
        print("Error: TINKER_API_KEY not found.")
        return

    print("Initializing ServiceClient...")
    service_client = tinker.ServiceClient(api_key=api_key)

    try:
        # Full path from list_user_checkpoints
        model_path = "tinker://3136a33c-83e4-55d4-ba93-7688c8f7b2be:train:0/sampler_weights/generic-human-v2"
        sampling_client = service_client.create_sampling_client(model_path=model_path)
    except Exception as e:
        print(f"Failed to create sampling client: {e}")
        print("Listing available models...")
        rest_client = service_client.create_rest_client()
        print("Calling list_user_checkpoints...")
        try:
            checkpoints = rest_client.list_user_checkpoints().result()
            print("Checkpoints:", checkpoints)
            # Print names/paths
            for cp in checkpoints:
                # Inspect checkpoint object
                print(f"Checkpoint: {cp}")
        except Exception as e:
            print(f"Error listing checkpoints: {e}")
        return

    print("Getting Tokenizer...")
    # We might need a training client to get the tokenizer if sampling client doesn't have it
    # But let's check if we can get it from sampling client first (it wasn't in inspect output but maybe it's there)
    if hasattr(sampling_client, 'get_tokenizer'):
        tokenizer = sampling_client.get_tokenizer()
    else:
        print("SamplingClient has no get_tokenizer. Creating TrainingClient for tokenizer...")
        training_client = service_client.create_lora_training_client(base_model="meta-llama/Llama-3.1-8B")
        tokenizer = training_client.get_tokenizer()

    print("Tokenizing prompt...")
    prompt_text = "User: Hello!\nCaz:"
    tokens = tokenizer.encode(prompt_text)
    model_input = types.ModelInput.from_ints(tokens)

    print("Sampling...")
    sampling_params = types.SamplingParams(max_tokens=20, temperature=0.7)
    future = sampling_client.sample(prompt=model_input, num_samples=1, sampling_params=sampling_params)
    result = future.result()

    print("Result Type:", type(result))
    print("Result Fields:", result.model_dump().keys())
    print("Sequences:", result.sequences)
    
    # Check if sequences are strings or tokens
    if isinstance(result.sequences[0], str):
        print("Output is String:", result.sequences[0])
    elif isinstance(result.sequences[0], list):
        print("Output is Tokens:", result.sequences[0])
        decoded = tokenizer.decode(result.sequences[0])
        print("Decoded:", decoded)
    else:
        print("Unknown output format:", result.sequences[0])

if __name__ == "__main__":
    test_tinker()
