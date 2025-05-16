import os
import sys
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from dotenv import load_dotenv

# Add project root to sys.path for agent_manager import
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
sys.path.append(PROJECT_ROOT)

# Conditional import for AgentManager
try:
    from agents.agent_manager import AgentManager
except ImportError:
    print("Warning: Could not import AgentManager. Ensure it's correctly placed and has no import errors.")
    AgentManager = None 

# Load environment variables
dotenv_path = os.path.join(PROJECT_ROOT, '.env')
load_dotenv(dotenv_path=dotenv_path)

# --- Pydantic Models ---
class Message(BaseModel):
    role: str
    content: str

class ImageSource(BaseModel):
    type: str = "base64"
    media_type: str
    data: str

class ChatRequest(BaseModel):
    query: str
    agent_type: str = "financial_assistant"
    history: Optional[List[Message]] = Field(default_factory=list)
    image: Optional[ImageSource] = None

class ChatResponse(BaseModel):
    response: str
    tool_outputs: Optional[List[Dict]] = Field(default_factory=list)

# --- FastAPI App Setup ---
app = FastAPI(
    title="Finance Agent API V2",
    docs_url=None,
    redoc_url=None
)


# --- CORS Middleware Configuration ---
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],       
#     allow_methods=["*"],
#     allow_headers=["*"],
#     allow_credentials=False,
# )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or specify ngrok + localhost if you want to be strict
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Health Check Endpoint ---
@app.get("/")
async def read_root():
    return {"message": "Finance Agent API is running."}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# --- API Endpoint ---
@app.post("/chat", response_model=ChatResponse)
async def handle_chat(request_data: ChatRequest):
    print(f"API: /chat endpoint hit. Request query: '{request_data.query}', agent_type: '{request_data.agent_type}'")
    if AgentManager is None:
        print("API: Error - AgentManager module was not imported successfully.")
        raise HTTPException(status_code=503, detail="AgentManager is not initialized. Check server logs for import errors.")

    agent_manager = None 
    try:
        print(f"API: Attempting to initialize AgentManager for agent_type: '{request_data.agent_type}'")
        agent_manager = AgentManager(agent_type=request_data.agent_type)
        print("API: AgentManager initialized successfully.")
        
        history_for_agent = [{"role": msg.role, "content": msg.content} for msg in request_data.history] if request_data.history else []

        print(f"API: Attempting to process query: '{request_data.query}' with history_length: {len(history_for_agent)}")
        processed_output = agent_manager.process_query(
                                                request_data.query,
                                                history=history_for_agent,
                                                image=request_data.image.dict() if request_data.image else None
                                            )

        
        response_text = processed_output.get("text_response", "Agent processed the request but did not generate a specific text response.")
        tool_outputs_data = processed_output.get("tool_outputs", [])

        print(f"API: Query processed. Text response from agent: '{response_text}', Tool outputs count: {len(tool_outputs_data)}")
        
        print(f"API: Sending final response. Text: '{response_text}', Tool Outputs: {tool_outputs_data}")
        return ChatResponse(response=response_text, tool_outputs=tool_outputs_data)
    
    except ValueError as ve: 
        print(f"API: ValueError during AgentManager operation: {ve}")
        raise HTTPException(status_code=500, detail=f"Configuration error: {str(ve)}")
    except ImportError as ie:
        print(f"API: ImportError during AgentManager usage: {ie}")
        raise HTTPException(status_code=500, detail=f"Internal server error related to agent processing (ImportError): {ie}")
    except Exception as e:
        print(f"API: Unhandled exception during chat handling: {e}")
        import traceback
        print(traceback.format_exc()) 
        if agent_manager:
            print(f"API: AgentManager state before error: type={agent_manager.agent_type}, tools_loaded={len(agent_manager.tools) if hasattr(agent_manager, 'tools') else 'N/A'}")
        else:
            print("API: AgentManager was not successfully initialized before the error.")
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

# --- How to Run ---
# From the project root directory (super_agent):
# source agenv/bin/activate
# uvicorn finance_agents.api:app --host 0.0.0.0 --port 5050 --reload