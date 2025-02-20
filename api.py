from fastapi import FastAPI
from pydantic import BaseModel
from agents.agent_manager import AgentManager

# Initialize FastAPI app
app = FastAPI(title="Market Insight API", description="An API for querying financial insights", version="1.0")

# Initialize the agent
agent = AgentManager()

# Request model for API
class QueryRequest(BaseModel):
    query: str

@app.post("/query")
def query_agent(request: QueryRequest):
    """Handles user queries and returns structured responses."""
    response = agent.process_query(request.query)
    return {"response": response}

# Root endpoint
@app.get("/")
def home():
    return {"message": "Market Insight API is running. Use /query to ask questions."}
