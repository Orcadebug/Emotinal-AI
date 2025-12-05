import os
import tinker
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("TINKER_API_KEY")
if not api_key:
    print("TINKER_API_KEY not found in environment.")
    exit(1)

print(f"Using API Key: {api_key[:5]}...")

try:
    service_client = tinker.ServiceClient(api_key=api_key)
    rest_client = service_client.create_rest_client()
    checkpoints_response = rest_client.list_user_checkpoints().result()
    
    print("\nAvailable Checkpoints:")
    found = False
    for cp in checkpoints_response.checkpoints:
        print(f"- ID: {cp.checkpoint_id}, Type: {cp.checkpoint_type}, Path: {cp.tinker_path}")
        if "generic-human-v2" in cp.checkpoint_id and cp.checkpoint_type == "sampler":
            found = True
            
    if found:
        print("\nSUCCESS: Found 'generic-human-v2' sampler checkpoint.")
    else:
        print("\nFAILURE: Did NOT find 'generic-human-v2' sampler checkpoint.")

except Exception as e:
    print(f"\nError: {e}")
