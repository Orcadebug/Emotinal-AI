import requests
import time
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BASE_URL = os.getenv("BRAIN_API_URL", "http://localhost:8000")
API_KEY = os.getenv("BRAIN_API_KEY", "my-secret-key-123")

def chat(session_id, message):
    url = f"{BASE_URL}/chat"
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": API_KEY
    }
    payload = {
        "user_id": session_id, # Now acts as session_id
        "message": message
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error: {e}")
        if hasattr(e, 'response') and e.response is not None:
             print(f"Server returned: {e.response.text}")
        return None

def run_test():
    print("--- Starting Identity Flow Test ---")
    
    # 1. New Session
    session_id = f"test_session_{int(time.time())}"
    print(f"\n[Step 1] New Session: {session_id}")
    
    resp = chat(session_id, "Hello there!")
    print(f"User: Hello there!")
    print(f"Brain: {resp['response']}")
    
    if "Who is this?" in resp['response']:
        print("✅ PASS: Brain asked for identity.")
    else:
        print("❌ FAIL: Brain did not ask for identity.")

    # 2. Identify
    print(f"\n[Step 2] Identify as 'Tester'")
    resp = chat(session_id, "It's Tester")
    print(f"User: It's Tester")
    print(f"Brain: {resp['response']}")
    
    if "Tester" in resp['response']:
        print("✅ PASS: Brain acknowledged identity.")
    else:
        print("❌ FAIL: Brain did not acknowledge identity.")

    # 3. Normal Chat
    print(f"\n[Step 3] Normal Chat")
    resp = chat(session_id, "How are you?")
    print(f"User: How are you?")
    print(f"Brain: {resp['response']}")
    
    if "Who is this?" not in resp['response']:
        print("✅ PASS: Brain remembers identity.")
    else:
        print("❌ FAIL: Brain forgot identity.")

    print("\n--- Test Complete ---")

if __name__ == "__main__":
    run_test()
