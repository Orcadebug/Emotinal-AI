from fastapi import FastAPI, HTTPException, Depends, Request, Security
from fastapi.security.api_key import APIKeyHeader, APIKeyQuery
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from brain import Brain
from voice_router import router as voice_router
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# --- Security ---
API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)
api_key_query = APIKeyQuery(name="key", auto_error=False)

BRAIN_API_KEY = os.environ.get("BRAIN_API_KEY")

async def get_api_key(
    api_key_header: str = Security(api_key_header),
    api_key_query: str = Security(api_key_query),
):
    if not BRAIN_API_KEY:
        # If no key set on server, allow all (dev mode)
        return True
        
    if api_key_header == BRAIN_API_KEY or api_key_query == BRAIN_API_KEY:
        return api_key_header or api_key_query
        
    raise HTTPException(
        status_code=403,
        detail="Could not validate credentials",
    )

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
def chat(request: ChatRequest, api_key: str = Depends(get_api_key)):
    try:
        result = brain.process_message(request.user_id, request.message)
        return ChatResponse(response=result["response"], mood=result["mood"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
