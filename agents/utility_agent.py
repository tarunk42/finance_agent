import os
import sys

# Get the absolute path of the finance_agents directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from agents.agent_manager import AgentManager

if __name__ == "__main__":
    agent = AgentManager(agent_type="utility_assistant")  # Explicitly specify the agent type
    
    query = input("Ask your utility assistant: ")
    response = agent.process_query(query)
    
    print(response)

