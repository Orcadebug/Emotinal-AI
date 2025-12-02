import asyncio
import json
import base64
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List
import logging

# Try importing Chatterbox, handle failure gracefully for now
try:
    # from chatterbox.tts import ChatterboxTTS
    # model = ChatterboxTTS.from_pretrained(device="cpu") # Use CPU for safety first
    # For now, we'll mock it until installation completes and we verify it works
    model = None
    print("Chatterbox not yet loaded (installation pending).")
except ImportError:
    model = None
    print("Chatterbox not found.")

router = APIRouter()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_text(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def send_audio(self, audio_data: bytes, websocket: WebSocket):
        # Send as binary or base64? Let's use base64 JSON for metadata support
        encoded = base64.b64encode(audio_data).decode('utf-8')
        await websocket.send_json({"type": "audio", "data": encoded})

manager = ConnectionManager()

@router.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    # Check API Key from query param: /ws/chat?key=YOUR_KEY
    import os
    BRAIN_API_KEY = os.environ.get("BRAIN_API_KEY")
    
    if BRAIN_API_KEY:
        query_params = websocket.query_params
        key = query_params.get("key")
        if key != BRAIN_API_KEY:
            await websocket.close(code=1008) # Policy Violation
            return

    await manager.connect(websocket)
    brain = websocket.app.state.brain
    
    # Generate a temporary user ID for WebSocket connections if not provided
    # In a real app, we'd expect a handshake or token.
    user_id = "voice_user_1" 
    
    try:
        while True:
            data = await websocket.receive_text()
            # Expecting JSON: {"type": "text"|"audio"|"interrupt", "content": ...}
            try:
                message = json.loads(data)
            except json.JSONDecodeError:
                continue

            if message["type"] == "interrupt":
                # Stop any current generation/streaming
                logger.info("Interruption signal received.")
                # TODO: Implement cancellation logic
                continue

            if message["type"] == "text":
                user_text = message["content"]
                logger.info(f"Received text: {user_text}")
                
                # 1. Generate AI Response (Text) via Brain
                result = await brain.process_message_async(user_id, user_text)
                ai_text = result["response"]
                
                await manager.send_text(json.dumps({"type": "text", "content": ai_text, "mood": result["mood"]}), websocket)

                # 2. Generate Audio (TTS)
                try:
                    if model:
                        # Chatterbox implementation (if it ever works)
                        # wav = model.generate(ai_text)
                        # audio_bytes = wav.tobytes() 
                        # await manager.send_audio(audio_bytes, websocket)
                        pass
                    else:
                        # Fallback: gTTS
                        from gtts import gTTS
                        import io
                        
                        # Generate audio in memory
                        tts = gTTS(text=ai_text, lang='en')
                        mp3_fp = io.BytesIO()
                        tts.write_to_fp(mp3_fp)
                        mp3_fp.seek(0)
                        audio_bytes = mp3_fp.read()
                        
                        # Send to frontend
                        await manager.send_audio(audio_bytes, websocket)
                        logger.info("Sent audio response (gTTS).")
                        
                except Exception as e:
                    logger.error(f"TTS Error: {e}")

    except WebSocketDisconnect:
        manager.disconnect(websocket)
