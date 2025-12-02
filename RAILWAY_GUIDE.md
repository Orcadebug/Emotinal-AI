# Railway Setup & Integration Guide

This guide walks you through ensuring your Railway backend and storage are correctly set up and how to connect any frontend to your unified Brain API.

## Part 1: Railway Backend & Storage Setup

Since you are using Railway, your deployment is automated via GitHub.

### 1. Verify PostgreSQL Database
1.  Go to your **Railway Dashboard**.
2.  Open your project.
3.  Ensure you have a **PostgreSQL** service added.
4.  Click on the PostgreSQL service -> **Variables**.
5.  Copy the `DATABASE_URL`.

### 2. Verify Backend Service
1.  Click on your **Backend** service (the one connected to this GitHub repo).
2.  Go to **Variables**.
3.  Ensure the following variables are set:
    -   `DATABASE_URL`: (Paste the value from step 1).
    -   `TINKER_API_KEY`: Your Tinker AI API key.
    -   `HF_TOKEN`: Your Hugging Face User Access Token (Required for Llama 3).
    -   `BRAIN_API_KEY`: (Optional) Set this to a secret string (e.g., `my-secret-key-123`) to secure your API.
    -   `PORT`: Railway usually sets this automatically.

### 3. Verify Deployment
1.  Go to **Deployments** tab in your Backend service.
2.  You should see a new deployment building.
3.  Once "Active", click the **Public Domain** link.

---

## Part 2: Connecting a Frontend

### Option A: Using the Provided Next.js Frontend
1.  Navigate to `frontend/.env.local`.
2.  Set the API URL:
    ```env
    NEXT_PUBLIC_WS_URL=wss://your-project.up.railway.app/ws/chat?key=YOUR_BRAIN_API_KEY
    NEXT_PUBLIC_API_URL=https://your-project.up.railway.app
    ```

### Option B: Using a Different Frontend

**1. For Text Chat:**
-   **Endpoint**: `POST https://your-project.up.railway.app/chat`
-   **Headers**: `X-API-Key: YOUR_BRAIN_API_KEY` (or query param `?key=...`)
-   **JSON Body**:
    ```json
    {
      "user_id": "user123",
      "message": "Hello Brain!"
    }
    ```

**2. For Voice/Real-time:**
-   **Endpoint**: `wss://your-project.up.railway.app/ws/chat?key=YOUR_BRAIN_API_KEY`
-   **Protocol**: WebSocket

---

## Part 3: Connecting to ChatGPT (Custom GPT)

1.  Go to [ChatGPT](https://chat.openai.com) -> **Explore** -> **Create a GPT**.
2.  Go to **Configure** -> **Actions** -> **Create new action**.
3.  **Authentication**: Select **API Key** -> **Custom**.
    -   Header Name: `X-API-Key`
    -   Key: (The value you set for `BRAIN_API_KEY` in Railway)
4.  **Schema**: Paste the schema below:

```yaml
openapi: 3.1.0
info:
  title: Digital Organism Brain
  version: 1.0.0
servers:
  - url: https://your-project.up.railway.app
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

---

## Troubleshooting

### Error: `baseten/Meta-Llama-3-tokenizer is not a local folder...`
**Why?** Even though Tinker runs the model in the cloud, your backend needs to **tokenize** (convert text to numbers) your messages locally before sending them. It tries to download the tokenizer for Llama 3 from Hugging Face.
**The Issue:** Llama 3 is a "gated" model, meaning you need permission and a token to download even its tokenizer.

**Solution 1 (Recommended):**
1.  Get a [Hugging Face Token](https://huggingface.co/settings/tokens).
2.  Add `HF_TOKEN` to your Railway Variables.

**Solution 2 (Alternative):**
Use a public copy of the Llama 3 model that doesn't require a token.
1.  In Railway Variables, add `MODEL_NAME` = `NousResearch/Meta-Llama-3-8B`.
