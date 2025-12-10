# Unified Brain API Documentation

The Digital Organism's backend has been packaged into a unified "Brain" API. This API serves as the central intelligence for the organism, handling conversation, memory, emotional state, and voice interactions.

## Base URL
`http://localhost:8000` (Local) or your deployed URL.

## Endpoints

### 1. Chat (Text)
**POST** `/chat`

Send a text message to the brain and receive a text response.

**Request Body:**
```json
{
  "user_id": "unique_user_id",
  "message": "Hello, how are you?"
}
```

**Response:**
```json
{
  "response": "I am doing well, thank you.",
  "mood": "awake"
}
```

### 2. Voice Chat (WebSocket)
**WebSocket** `/ws/chat`

Real-time voice and text communication.

**Message Format (Client -> Server):**
```json
{
  "type": "text",
  "content": "Hello via voice interface"
}
```
*Note: Audio input is not yet fully implemented on the client side, sending text is preferred.*

**Message Format (Server -> Client):**
```json
{
  "type": "text",
  "content": "Response text",
  "mood": "awake"
}
```
```json
{
  "type": "audio",
  "data": "base64_encoded_mp3_data"
}
```

### 3. Status
**GET** `/`

Check if the brain is alive.

**Response:**
```json
{
  "status": "alive",
  "tinker_connected": true
}
```

## Integration Guide

### Python Client Example
```python
import requests

API_URL = "http://localhost:8000"

def chat_with_brain(message, user_id="user1"):
    response = requests.post(f"{API_URL}/chat", json={
        "user_id": user_id,
        "message": message
    })
    return response.json()

print(chat_with_brain("Hello!"))
```

### ChatGPT Integration
You can use the `/chat` endpoint as a tool or action in a custom GPT.
1.  Expose the API via ngrok or deploy it.
2.  Define the schema in ChatGPT Actions:
    ```yaml
    openapi: 3.1.0
    info:
      title: Digital Organism Brain
      version: 1.0.0
    servers:
      - url: https://your-api-url.com
    paths:
      /chat:
        post:
          operationId: chat
          summary: Chat with the digital organism
          requestBody:
            content:
              application/json:
                schema:
                  type: object
                  properties:
                    user_id:
                      type: string
                    message:
                      type: string
          responses:
            '200':
              description: Successful response
              content:
                application/json:
                  schema:
                    type: object
                    properties:
                      response:
                        type: string
                      mood:
                        type: string
    ```

## Running the Brain
To start the backend server:
```bash
uvicorn backend.main:app --reload
```
