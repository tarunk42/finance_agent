# main.py (top-level)
from api import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("finance_agents.api:app", host="0.0.0.0", port=5050, reload=True)
