from fastapi import FastAPI, HTTPException, Depends, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from brain import Brain
from voice_router import router as voice_router

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Brain
brain = Brain()
app.state.brain = brain

app.include_router(voice_router)

# --- Models ---
class ChatRequest(BaseModel):
    user_id: str
    message: str

class ChatResponse(BaseModel):
    response: str
    mood: str

# --- Routes ---
@app.get("/")
def read_root():
    return brain.status()

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        result = brain.process_message(request.user_id, request.message)
        return ChatResponse(response=result["response"], mood=result["mood"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
