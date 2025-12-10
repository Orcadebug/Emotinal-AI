# Brain API Usage Guide

This guide explains how to use your Digital Organism's "Brain" as a standalone API, similar to how you would use OpenAI's API. This allows you to connect any UI (web, mobile, desktop) to your Brain.

## 1. The Base URL

*   **Local Development**: `http://localhost:8000`
*   **Production (Railway)**: `https://your-project.up.railway.app` (Replace with your actual Railway URL)

## 2. Authentication

**None Required.** This is an open API. You do not need an API key.

## 3. The Chat Endpoint

This is the main endpoint to send a message to the Brain and get a response.

*   **URL**: `/chat`
*   **Method**: `POST`
*   **Content-Type**: `application/json`

### Request Body

```json
{
  "user_id": "session-id-123",
  "message": "Hello"
}
```

*   `user_id`: **Now acts as a Session ID**. You can generate a random UUID or use a device ID. The Brain will track the actual user identity internally.
*   `message`: The text you want to send.

### Response Body

```json
{
  "response": "Who is this?",
  "mood": "curious"
}
```

## 4. The Conversational Identity Flow

The Brain now learns who you are through conversation.

1.  **New Session**: When you start a new session (or after 4 hours of inactivity), the Brain will not know who you are.
2.  **The Prompt**: If you say "Hello", the Brain will likely reply: **"Who is this?"**
3.  **Identification**: You should reply naturally, e.g., **"It's Sai"** or **"I am Sai"**.
4.  **Recognition**: The Brain will link your session to your profile ("Sai") and remember you for the next 4 hours.
    *   *Note: It remembers your relationship score and past interactions.*

## 5. Code Examples

### JavaScript / TypeScript (Frontend UI)

Use this snippet in your React, Vue, or vanilla JS application.

```javascript
const API_URL = "https://your-project.up.railway.app"; // Your Backend URL

async function sendMessageToBrain(message) {
  try {
    const response = await fetch(`${API_URL}/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        user_id: "session-123", // Replace with actual session ID
        message: message
      })
    });

    if (!response.ok) {
      throw new Error(`API Error: ${response.statusText}`);
    }

    const data = await response.json();
    console.log("Brain says:", data.response);
    console.log("Current Mood:", data.mood);
    return data;
    
  } catch (error) {
    console.error("Failed to chat with brain:", error);
  }
}

// Usage
sendMessageToBrain("What is the meaning of life?");
```

### cURL (Terminal Testing)

You can test the API directly from your terminal:

```bash
curl -X POST "http://localhost:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{"user_id": "test-session", "message": "Hello Brain!"}'
```

## 5. How to Run the API

### Locally
1.  Make sure you are in the `digital-organism` directory.
2.  Ensure your `.env` file has `BRAIN_API_KEY` set.
3.  Run the server:
    ```bash
    uvicorn backend.main:app --reload
    ```
4.  Your API is now live at `http://localhost:8000`.

### On Railway (Cloud)
1.  Push your code to GitHub.
2.  Railway will automatically redeploy.
3.  Ensure `BRAIN_API_KEY` is set in your Railway Service Variables.
4.  Your API is live at your public Railway domain.
