"""
FastAPI backend for the shopping chat agent.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
from agent import ShoppingAgent
import os

app = FastAPI(title="Mobile Shopping Chat Agent")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize agent (with error handling)
try:
    agent = ShoppingAgent()
except ValueError as e:
    print(f"Warning: {e}")
    print("Please set GEMINI_API_KEY in your .env file")
    agent = None


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str
    phones: list
    type: str


@app.get("/")
async def read_root():
    """Serve the main HTML page."""
    return FileResponse("static/index.html")


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Handle chat messages."""
    if agent is None:
        raise HTTPException(
            status_code=500, 
            detail="AI agent not initialized. Please set GEMINI_API_KEY in environment variables."
        )
    
    try:
        result = agent.handle_query(request.message)
        
        # Format phones for display
        formatted_phones = [agent.format_phone_for_display(phone) for phone in result["phones"]]
        
        return ChatResponse(
            response=result["response"],
            phones=formatted_phones,
            type=result["type"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}


# Mount static files (must be after routes to avoid conflicts)
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=4000)

