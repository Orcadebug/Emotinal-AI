# Digital Organism - Current State & Architecture

## Overview
This is a conversational AI "Brain" deployed on Railway that uses a fine-tuned LLM (via Tinker) with biological state simulation and relationship memory. The Brain identifies users through conversation and maintains persistent relationships.

## Completed Features

### ✅ Conversational Identity System
- **Session-based authentication**: API accepts `user_id` as a session ID (not actual user identity)
- **Dynamic identification**: Brain asks "Who is this?" for new/expired sessions
- **Pattern matching**: Recognizes identity from phrases like "It's [Name]", "I am [Name]", or single-word responses
- **4-hour timeout**: Sessions expire after 4 hours of inactivity, requiring re-identification
- **Database**: `sessions` table links session IDs to user identities

### ✅ Biological State System
- **Adenosine accumulation**: Increases by 5% per message (0.05 per interaction)
- **Sleep threshold**: Organism sleeps when adenosine > 90% (~18 messages)
- **Sleep response**: Returns "Zzz... (The organism is sleeping)" when asleep
- **Database**: `biological_state` table tracks adenosine level and sleep mode

### ✅ Relationship Memory
- **Affinity tracking**: Each user has an affinity score that changes with interactions
- **Interaction count**: Tracks total messages per user
- **Hostility mode**: If affinity < -5.0, Brain refuses to talk
- **Name storage**: Remembers user names for personalized responses
- **Secret phrases**: Users can set secret phrases (future authentication feature)
- **Database**: `relationships` table stores per-user data

### ✅ LLM Integration (Tinker)
- **Model**: Fine-tuned checkpoint `generic-human-v2` on Llama 3.1/3.2
- **System prompt**: "You are Caz, a digital organism. You are curious, sometimes sassy, and always responsive."
- **Repetition penalty**: 1.2 to prevent hallucination loops
- **Response cleanup**: Strips excessive punctuation and empty outputs
- **Temperature**: 0.7 for balanced creativity

### ✅ API & Deployment
- **Endpoint**: `POST /chat` with JSON `{"user_id": "session-id", "message": "text"}`
- **Response**: `{"response": "text", "mood": "awake|asleep|hostile|curious|neutral"}`
- **CORS**: Enabled for all origins
- **No API key required**: Open API (optional `BRAIN_API_KEY` for future security)
- **Railway deployment**: Auto-deploys from GitHub main branch
- **Database**: PostgreSQL on Railway

## Current Issues & Limitations

### Known Bugs
- **No adenosine decay**: Organism stays asleep indefinitely (no background worker to reset)
- **Empty responses**: Model occasionally outputs "..." for short/confrontational inputs (improved but not perfect)

### Missing Features
- **Dream worker**: Background process to simulate sleep/wake cycles
- **Emotion engine**: Advanced neurochemistry simulation (exists in codebase but not integrated)
- **Voice interface**: WebSocket endpoint exists but TTS is basic (gTTS fallback)
- **Memory retrieval**: No long-term conversation history in prompts

## File Structure

### Backend (`/backend`)
- **`main.py`**: FastAPI app, routes, CORS, validation error handler
- **`brain.py`**: Core logic (identity, relationships, LLM generation, biological state)
- **`voice_router.py`**: WebSocket endpoint for voice chat (basic implementation)
- **`schema.sql`**: Database schema (sessions, relationships, biological_state, chat_logs)

### Frontend (`/frontend`)
- **Next.js app**: Voice orb interface (not actively maintained)
- **`utils/brain_client.ts`**: TypeScript client for HTTP and WebSocket

### Documentation
- **`API_USAGE_GUIDE.md`**: How to use the `/chat` endpoint
- **`RAILWAY_GUIDE.md`**: Deployment instructions
- **`ORGANIC_SYSTEM_GUIDE.md`**: Biological state system explanation
- **`EMOTIONAL_REACTIONS.md`**: Emotion engine design (not implemented)

## Next Steps (Potential)

### High Priority
1. **Adenosine decay worker**: Background job to reduce adenosine over time (e.g., -10% per hour)
2. **Wake command**: Allow manual wake-up via special message or admin endpoint
3. **Improve LLM responses**: Add conversation history to prompts for better context

### Medium Priority
4. **Emotion integration**: Connect `emotion_engine/` modules to response generation
5. **Voice improvements**: Better TTS (Resemble AI or ElevenLabs)
6. **Admin dashboard**: View/reset biological state, manage users

### Low Priority
7. **Multi-model support**: Switch between different fine-tuned checkpoints
8. **Analytics**: Track conversation metrics, affinity trends
9. **Security**: Enforce `BRAIN_API_KEY` for production use

## Environment Variables (Railway)

Required:
- `DATABASE_URL`: PostgreSQL connection string (auto-set by Railway)
- `TINKER_API_KEY`: Tinker AI API key
- `HF_TOKEN`: Hugging Face token (for Llama tokenizer)

Optional:
- `MODEL_NAME`: Base model (default: `meta-llama/Llama-3.1-8B`)
- `BRAIN_API_KEY`: API key for authentication (currently unused)

## Testing

### Manual Testing
```bash
# Test identity flow
curl -X POST "https://emotinal-ai-production.up.railway.app/chat" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test-session-1", "message": "Hello"}'
# Expected: {"response": "Who is this?", "mood": "curious"}

curl -X POST "https://emotinal-ai-production.up.railway.app/chat" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test-session-1", "message": "It'\''s Sai"}'
# Expected: {"response": "Hello Sai. I remember you.", "mood": "neutral"}
```

### Automated Tests
- `tests/test_identity_flow.py`: Session identity tests (exists but may need updates)
- `backend/test_gatekeeper.py`: Biological state tests (sleep, hostility)

## Recent Changes (This Session)

1. **Fixed ImportError on Railway**: Added try/except for relative imports
2. **Added debug logging**: 422 errors now log request body for debugging
3. **Fixed model hallucination**: Added repetition penalty and response cleanup
4. **Improved prompt**: Added system instruction to make AI more responsive
5. **Updated documentation**: Created this comprehensive plan

---

**Last Updated**: 2025-12-08  
**Status**: Production-ready with known limitations  
**Deployment**: https://emotinal-ai-production.up.railway.app
