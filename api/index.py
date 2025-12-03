"""
Vercel serverless function handler for FastAPI app.
"""
import os
import sys

# Add parent directory to path to import modules
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

try:
    from agent import ShoppingAgent
except ImportError as e:
    print(f"Import error: {e}")
    ShoppingAgent = None

# Create FastAPI app
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
agent = None
try:
    if ShoppingAgent:
        agent = ShoppingAgent()
        print("✅ Agent initialized successfully")
    else:
        print("❌ ShoppingAgent not available")
except Exception as e:
    print(f"❌ Agent initialization failed: {str(e)}")
    import traceback
    traceback.print_exc()


class ChatRequest(BaseModel):
    message: str


@app.get("/")
async def read_root():
    """Serve the main HTML page."""
    try:
        static_path = os.path.join(parent_dir, "static", "index.html")
        if os.path.exists(static_path):
            return FileResponse(static_path)
        else:
            return JSONResponse(
                content={"error": "Static files not found"},
                status_code=404
            )
    except Exception as e:
        return JSONResponse(
            content={"error": str(e)},
            status_code=500
        )


@app.post("/api/chat")
async def chat(request: ChatRequest):
    """Handle chat messages."""
    if agent is None:
        return JSONResponse(
            status_code=500,
            content={
                "response": "AI agent not initialized. Please set GEMINI_API_KEY in Vercel environment variables.",
                "phones": [],
                "type": "error"
            }
        )
    
    try:
        result = agent.handle_query(request.message)
        
        # Format phones for display
        formatted_phones = [agent.format_phone_for_display(phone) for phone in result["phones"]]
        
        return {
            "response": result["response"],
            "phones": formatted_phones,
            "type": result["type"]
        }
    except Exception as e:
        error_msg = str(e)
        print(f"Error in chat endpoint: {error_msg}")
        import traceback
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={
                "response": f"Error processing query: {error_msg[:200]}",
                "phones": [],
                "type": "error"
            }
        )


@app.get("/api/health")
async def health():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "agent_initialized": agent is not None,
        "python_version": sys.version
    }


# Serve static files
static_dir = os.path.join(parent_dir, "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")


# Vercel expects the app to be exported
# For FastAPI, Vercel's Python runtime will automatically handle it
# But we can also create a handler function if needed
def handler(request):
    """Alternative handler for Vercel (if needed)."""
    return app
