import os
import asyncio
import re # Import regex module
import json # Import JSON module
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from typing import List, Dict, Optional, Any, Union # Add Any, Union
from agents.agent_manager import AgentManager

# Load environment variables from .env file at the project root
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=dotenv_path)

# --- Pydantic Models for Request/Response ---

# Define structures for multimodal content parts
class TextPart(BaseModel):
    type: str = "text"
    text: str

class ImageSource(BaseModel):
    type: str = "base64"
    media_type: str # e.g., "image/jpeg", "image/png"
    data: str # Base64 encoded string

class ImagePart(BaseModel):
    type: str = "image"
    source: ImageSource

class ChatMessage(BaseModel):
    role: str
    # Content can be a simple string or a list of text/image parts
    content: Union[str, List[Union[TextPart, ImagePart]]]

class ChatRequest(BaseModel):
    query: str # The primary text query
    conversation_id: str
    history: Optional[List[ChatMessage]] = None # Allow optional history override
    image_data: Optional[str] = None # Optional base64 encoded image data
    image_media_type: Optional[str] = None # Required if image_data is present, e.g., "image/jpeg"

class ChatResponse(BaseModel):
    response: str # Natural language response
    conversation_id: str
    structured_data: Optional[Any] = None # Add field for structured data
    # Optionally return history:
    # history: List[ChatMessage] = Field(default_factory=list)

# --- FastAPI App Setup ---
app = FastAPI(title="Multi-Agent API")

# --- CORS Middleware Configuration (Simplified for Debugging) ---
# Allow all origins, methods, and headers.
# WARNING: This is insecure for production environments.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow any origin
    allow_credentials=False, # Set to False when using wildcard origin
    allow_methods=["*"], # Allow all methods
    allow_headers=["*"], # Allow all headers
)

# --- In-memory History Store ---
# Removed application-specific in-memory history store

# --- API Endpoint ---
@app.post("/chat", response_model=ChatResponse)
async def handle_chat(request_data: ChatRequest):
    """
    API endpoint to interact with the orchestrated agent system using FastAPI.
    """
    # Simulate processing the request
    response_text = f"Received your message: {request_data.query}"
    conversation_id = request_data.conversation_id

    # Return a response with the received message and conversation ID
    return ChatResponse(
        response=response_text,
        conversation_id=conversation_id,
        structured_data=None  # You can populate this if needed
    )


# --- How to Run ---
# Use Uvicorn to run the FastAPI application:
# Ensure virtual environment is active (`source env/bin/activate`)
# From the project root directory (`TestProj90`):
# uvicorn src.api:app --host 127.0.0.1 --port 5000 --reload
#
# --reload flag automatically restarts the server when code changes (useful for development)