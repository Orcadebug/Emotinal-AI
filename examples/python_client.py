import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

def chat_with_brain(message, user_id="client_user"):
    # 1. Get Configuration from Environment Variables
    api_url = os.getenv("BRAIN_API_URL")

    if not api_url:
        print("Error: BRAIN_API_URL environment variable is not set.")
        print("Please set it to your deployed backend URL (e.g., https://your-project.up.railway.app)")
        return

    # Ensure URL doesn't have a trailing slash
    api_url = api_url.rstrip("/")

    # 2. Prepare the Request
    endpoint = f"{api_url}/chat"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    payload = {
        "user_id": user_id,
        "message": message
    }

    print(f"Sending message to {endpoint}...")
    
    # 3. Send the Request
    try:
        response = requests.post(endpoint, headers=headers, json=payload)
        response.raise_for_status() # Raise error for bad status codes
        
        data = response.json()
        
        # 4. Process Response
        print("\n--- Brain Response ---")
        print(f"Mood: {data.get('mood')}")
        print(f"Response: {data.get('response')}")
        print("----------------------\n")
        
        return data

    except requests.exceptions.RequestException as e:
        print(f"\nError communicating with Brain: {e}")
        if hasattr(e, 'response') and e.response is not None:
             print(f"Server returned: {e.response.text}")

if __name__ == "__main__":
    # Example Usage
    print("Brain Client Example")
    print("--------------------")
    user_input = input("Enter a message for the brain: ")
    if user_input:
        chat_with_brain(user_input)
