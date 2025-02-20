import sys
import os

# Get the absolute path of the finance_agents directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import AIMessage
import config
from config import SYSTEM_PROMPTS, TOOL_REGISTRY
from tools import *


class AgentManager:
    """Manages the Market Insights Agent and tool execution."""

    def __init__(self):
        # Load system prompt
        self.system_prompt = SYSTEM_PROMPTS["financial_assistant"]

        # Dynamically load tools
        self.tools = []
        for tool_name in TOOL_REGISTRY:
            tool_class = globals().get(tool_name, None)  # Safe lookup
            if tool_class:
                self.tools.append(tool_class())
        
        # Log which tools are loaded
        print(f"Loaded Tools: {[tool.name for tool in self.tools]}")

        # Initialize LLM
        self.model = ChatOpenAI(
            model=config.OPENAI_MODEL,
            api_key=config.OPENAI_API_KEY
        )
        
        # Create ReAct agent
        self.agent = create_react_agent(
            model=self.model,
            tools=self.tools
        )


    def process_query(self, query: str):
        """Executes the agent with a given query and formats the response."""
        print(f"🔍 Processing Query: {query}")

        chunks = self.agent.stream({
            "messages": [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": query}
            ]
        })
        
        formatted_response = []
        for chunk in chunks:
            print(f"🛠️ Debug: {chunk}")  # Log raw response from agent
            if "agent" in chunk and "messages" in chunk["agent"]:
                last_message = chunk["agent"]["messages"][-1]
                if isinstance(last_message, AIMessage):
                    formatted_response.append(last_message.content)
                else:
                    formatted_response.append("No valid AI response.")

        return "\n".join(formatted_response)


