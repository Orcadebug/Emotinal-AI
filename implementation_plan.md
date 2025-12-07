# Implementation Plan - Conversational Identity

The goal is to allow the Brain to identify users through conversation rather than relying on a fixed API key or user ID. The Brain will ask "Who is this?" at the start of a session or after 4 hours of inactivity.

## User Review Required

> [!IMPORTANT]
> This change modifies the core `process_message` flow. The `user_id` passed to the API will now be treated as a **Session ID**. The actual user identity (name, affinity, memory) will be resolved dynamically.

## Proposed Changes

### Backend

#### [MODIFY] [brain.py](file:///Users/saipittala/HRM model (Quants)/digital-organism/backend/brain.py)

1.  **Database Schema**:
    *   Add `sessions` table:
        *   `session_id` (TEXT PRIMARY KEY)
        *   `user_id` (TEXT, Foreign Key to `relationships.user_id`, nullable)
        *   `last_active` (TIMESTAMP)
        *   `created_at` (TIMESTAMP)

2.  **Session Management**:
    *   Implement `get_or_create_session(session_id)`:
        *   Returns session data.
        *   If session exists but `last_active` > 4 hours ago, reset `user_id` to NULL (force re-identification).

3.  **Message Processing (`process_message`)**:
    *   **Step 1**: Retrieve Session.
    *   **Step 2**: Check Identity State.
        *   If `session.user_id` is NULL:
            *   Check if message looks like an answer (e.g., "It's Sai", "I am Sai", "Sai").
            *   If match found:
                *   Link session to user "Sai".
                *   Reply: "Hello Sai. [Personalized Greeting]"
            *   If no match:
                *   Reply: "Who is this?"
                *   (Stop processing)
        *   If `session.user_id` is SET:
            *   **CRITICAL**: Load `relationships` data (affinity, name, secret) for this `user_id`.
            *   **Preserve Existing Logic**: Use the loaded `affinity` to determine mood/hostility (e.g., if affinity < -5.0, be hostile).
            *   Process message normally using the resolved identity.

## Verification Plan

### Automated Tests
*   I will create a reproduction script `tests/test_identity_flow.py` to simulate the conversation flow:
    1.  Start new session -> Expect "Who is this?" (or similar prompt if I trigger it).
    2.  Send "It's TestUser" -> Expect "Hello TestUser".
    3.  Send "Hello" -> Expect normal response.
    4.  Simulate 4 hour delay -> Send "Hello" -> Expect "Who is this?".

### Manual Verification
*   Run the server and use the `examples/python_client.py` to chat.
*   Verify the "Who is this?" prompt appears for a new session.
