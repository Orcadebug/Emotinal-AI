# Frontend Integration Guide

This guide explains how to connect **any** frontend (React, Vue, etc.) to your Digital Organism's Brain API using the `BrainClient` helper.

## 1. Get the Brain Client
Copy the `BrainClient` class from `frontend/utils/brain_client.ts` into your project (e.g., `src/utils/brain_client.ts`).

## 2. Initialize the Client
In your main component or service, initialize the client with your Railway URL.

```typescript
import { BrainClient } from "./utils/brain_client";

// Use your Railway URL (e.g., https://your-project.up.railway.app)
const brain = new BrainClient("https://your-project.up.railway.app");
```

## 3. Connect via WebSocket (Voice/Real-time)
To enable real-time communication (like the Orb interface):

```typescript
brain.connectWebSocket(
  (data) => {
    // Handle incoming messages
    if (data.type === "text") {
      console.log("AI said:", data.content);
    } else if (data.type === "audio") {
      // Play audio data (base64)
      playAudio(data.data);
    }
  },
  () => console.log("Connected!"), // On Open
  () => console.log("Disconnected") // On Close
);
```

## 4. Send Messages
To send what the user says (or types):

```typescript
// Send text via WebSocket (preferred for voice chat)
brain.sendWsText("Hello, are you there?");

// OR Send via REST API (for simple text chat)
const response = await brain.sendText("user123", "Hello!");
console.log(response.response);
```

## 5. Interrupting
If the user starts speaking while the AI is talking:

```typescript
brain.interrupt();
```

## Example: React Hook
You can wrap this in a `useEffect` hook:

```typescript
useEffect(() => {
  const brain = new BrainClient("https://your-project.up.railway.app");
  brain.connectWebSocket((data) => {
    // Update state
  });
  
  return () => brain.disconnect();
}, []);
```
