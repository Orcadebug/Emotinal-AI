import os
import requests
import json
from dotenv import load_dotenv

load_dotenv("backend/.env")

API_KEY = os.getenv("TINKER_API_KEY")
# User provided URL + standard API suffix guess
BASE_URL = "https://thinkingmachines.ai/tinker/api/v1" 

def upload_and_train():
    if not API_KEY or API_KEY == "your_tinker_api_key_here":
        print("Error: TINKER_API_KEY is missing in backend/.env")
        print("Please set your API key and try again.")
        return

    headers = {"Authorization": f"Bearer {API_KEY}"}
    
    # 1. Upload File
    print("Uploading merged_training_data.jsonl...")
    file_path = "merged_training_data.jsonl"
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found. Run prepare_data.py first.")
        return

    try:
        with open(file_path, 'rb') as f:
            files = {'file': f}
            # Hypothetical endpoint for file upload
            response = requests.post(f"{BASE_URL}/files", headers=headers, files=files)
            response.raise_for_status()
            file_id = response.json()['id']
            print(f"File uploaded successfully. ID: {file_id}")
    except Exception as e:
        print(f"Upload failed: {e}")
        print("Note: The Tinker API URL is a placeholder. Please check documentation.")
        return

    # 2. Start Fine-Tuning
    print("Starting Fine-Tuning Job...")
    payload = {
        "model": "llama-3-8b-base",
        "training_file": file_id,
        "suffix": "generic-human-v1"
    }
    
    try:
        # Hypothetical endpoint for fine-tuning
        response = requests.post(f"{BASE_URL}/fine_tuning/jobs", headers=headers, json=payload)
        response.raise_for_status()
        job_id = response.json()['id']
        print(f"Fine-tuning job started! ID: {job_id}")
        print("Monitor progress in your Tinker dashboard.")
    except Exception as e:
        print(f"Job start failed: {e}")

if __name__ == "__main__":
    upload_and_train()
