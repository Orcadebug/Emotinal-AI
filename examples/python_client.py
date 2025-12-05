import requests
import os

# Configuration
API_URL = "http://localhost:8000" # Or your Railway URL: https://your-project.up.railway.app
API_KEY = "my-secret-key-123"     # The BRAIN_API_KEY you set in Railway

def chat_with_brain(message, user_id="external_app_1"):
    """
    Sends a message to the Brain API and prints the response.
    """
    print(f"Sending: '{message}'...")
    
    try:
        response = requests.post(
            f"{API_URL}/chat",
            headers={"X-API-Key": API_KEY},
            json={
                "user_id": user_id,
                "message": message
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"Brain ({data['mood']}): {data['response']}")
            return data
        else:
            print(f"Error {response.status_code}: {response.text}")
            
    except Exception as e:
        print(f"Connection Error: {e}")

if __name__ == "__main__":
    # Test the connection
    chat_with_brain("Hello! I am connecting from a Python script.")
