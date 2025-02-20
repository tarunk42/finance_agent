import os
import sys

# Get the absolute path of the finance_agents directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from agents.agent_manager import AgentManager

if __name__ == "__main__":
    agent = AgentManager()
    
    query = input("Ask your financial assistant: ")
    response = agent.process_query(query)
    
    print(response)
