from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from enhanced_neurochemistry import EnhancedNeurochemistryEngine
import json
import uvicorn
import os

app = FastAPI(title="Enhanced Emotion Engine MCP Server")
engine = EnhancedNeurochemistryEngine()

# Load baseline memories on startup
@app.on_event("startup")
async def load_baseline():
    baseline_path = "../data/baseline_memories.json"
    if os.path.exists(baseline_path):
        with open(baseline_path, 'r') as f:
            baseline_data = json.load(f)
        engine.memory.implant_baseline_memories(baseline_data)
        print(f"✓ Loaded {len(baseline_data)} baseline memories")
    else:
        print("⚠ No baseline memories found")

@app.get("/")
async def root():
    return {"status": "running", "service": "emotion_engine"}

@app.get("/mcp/tools")
async def get_tools():
    """MCP tool discovery endpoint"""
    return {
        "tools": [
            {
                "name": "get_emotional_state",
                "description": "Get current neurochemistry state",
                "parameters": {}
            },
            {
                "name": "update_emotion",
                "description": "Update emotional state based on interaction",
                "parameters": {
                    "reward": {"type": "number", "description": "Reward signal (0-1)"},
                    "stress": {"type": "number", "description": "Stress signal (0-1)"},
                    "social": {"type": "number", "description": "Social signal (0-1)"},
                    "novelty": {"type": "number", "description": "Novelty signal (0-1)"},
                    "user_input": {"type": "string", "description": "User input text"}
                }
            },
            {
                "name": "get_generation_context",
                "description": "Get full context including memories and curiosity for generation",
                "parameters": {
                    "user_input": {"type": "string", "description": "User input text"}
                }
            },
            {
                "name": "get_full_status",
                "description": "Get comprehensive status of all emotional systems",
                "parameters": {}
            }
        ]
    }

@app.post("/mcp/call/{tool_name}")
async def call_tool(tool_name: str, params: dict):
    """MCP tool execution endpoint"""
    if tool_name == "get_emotional_state":
        return {
            "state": engine.get_state(),
            "tokens": engine.get_conditioning_tokens()
        }
    elif tool_name == "update_emotion":
        new_state = engine.update(
            reward=params.get("reward", 0.0),
            stress=params.get("stress", 0.0),
            social=params.get("social", 0.0),
            novelty=params.get("novelty", 0.0),
            user_input=params.get("user_input", "")
        )
        return {
            "state": new_state,
            "tokens": engine.get_conditioning_tokens()
        }
    elif tool_name == "get_generation_context":
        context = engine.get_context_for_generation(params.get("user_input", ""))
        return context
    elif tool_name == "get_full_status":
        return engine.get_full_status()
    else:
        return JSONResponse(status_code=404, content={"error": "Tool not found"})

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket for real-time state updates"""
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            
            if data.get("action") == "get_state":
                await websocket.send_json({
                    "state": engine.get_state(),
                    "tokens": engine.get_conditioning_tokens()
                })
            elif data.get("action") == "update":
                new_state = engine.update(
                    reward=data.get("reward", 0.0),
                    stress=data.get("stress", 0.0),
                    social=data.get("social", 0.0),
                    novelty=data.get("novelty", 0.0),
                    user_input=data.get("user_input", "")
                )
                await websocket.send_json({
                    "state": new_state,
                    "tokens": engine.get_conditioning_tokens()
                })
            elif data.get("action") == "get_context":
                context = engine.get_context_for_generation(data.get("user_input", ""))
                await websocket.send_json(context)
            elif data.get("action") == "get_status":
                status = engine.get_full_status()
                await websocket.send_json(status)
    except WebSocketDisconnect:
        print("Client disconnected")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
