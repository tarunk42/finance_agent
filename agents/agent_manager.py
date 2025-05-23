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
    """Manages specialized agents and tool execution."""

    def __init__(self, agent_type="financial_assistant"):
        """Initialize the agent with the appropriate system prompt."""
        self.agent_type = agent_type
        self.system_prompt = SYSTEM_PROMPTS.get(agent_type, "You are an AI assistant.")  # Default if not found

        # Dynamically load relevant tools
        self.tools = []
        for tool_name in TOOL_REGISTRY:
            tool_class = globals().get(tool_name, None)  
            if tool_class:
                self.tools.append(tool_class())

        print(f"🔧 Loaded Tools: {[tool.name for tool in self.tools]}")

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

    def process_query(self, query: str, history: list = None, image: dict = None):
        """Processes a query using the correct system prompt and optional history."""
        print(f"🔍 Processing Query: '{query}' with history length: {len(history) if history else 0}")

        messages_for_agent = []
        # Add system prompt first
        messages_for_agent.append({"role": "system", "content": self.system_prompt})
        
        # Add existing history
        if history:
            messages_for_agent.extend(history)
        
        # Prepare content for the user's message
        user_message_content = []
        if query: # Add text part if query is not empty
            user_message_content.append({"type": "text", "text": query})

        if image:
            user_message_content.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:{image['media_type']};base64,{image['data']}"
                }
            })
        
        # Add current user query (with image if present)
        if user_message_content: # Only add if there's text or an image
            messages_for_agent.append({"role": "user", "content": user_message_content})
        elif not query and not image: # Handle case where both query and image are empty, though frontend should prevent this
            print("AgentManager: Warning - process_query called with empty query and no image.")
            # Decide on behavior: maybe return an error or a default message
            # For now, let's allow it to proceed, agent might handle empty input.
            # Or, append an empty user message if required by the agent structure:
            # messages_for_agent.append({"role": "user", "content": ""})
            pass


        
        print(f"AgentManager: Total messages being sent to agent: {len(messages_for_agent)}")
        # For debugging, you might want to print the full messages_for_agent if issues persist
        # for i, msg in enumerate(messages_for_agent):
        #     print(f"  Msg {i}: Role='{msg['role']}', Content='{msg['content'][:100]}...'")


        chunks = self.agent.stream({"messages": messages_for_agent})
        
        formatted_response = []
        tool_outputs = [] # To store data from tool calls
        import json # Ensure json is imported

        for chunk in chunks:
            print(f"🛠️ Debug: {chunk}")
            if "agent" in chunk and "messages" in chunk["agent"]:
                last_message = chunk["agent"]["messages"][-1]
                if isinstance(last_message, AIMessage):
                    formatted_response.append(last_message.content)
                    # print("\n\n\nChunk size:", len(last_message.content), "\n\n\n\n") # Debugging line for chunk size
                # else: # No need for "No valid AI response" here as we only care about AIMessage content for final response
                #     formatted_response.append("No valid AI response.")
            elif "tools" in chunk and "messages" in chunk["tools"]:
                for tool_message in chunk["tools"]["messages"]:
                    if hasattr(tool_message, 'content') and hasattr(tool_message, 'name'):
                        try:
                            # Attempt to parse the JSON content of the tool message
                            tool_data_content = json.loads(tool_message.content)
                            tool_outputs.append({
                                "tool_name": tool_message.name,
                                "tool_call_id": tool_message.tool_call_id if hasattr(tool_message, 'tool_call_id') else None,
                                "data": tool_data_content
                            })
                        except json.JSONDecodeError:
                            # If content is not valid JSON, store it as a raw string
                            tool_outputs.append({
                                "tool_name": tool_message.name,
                                "tool_call_id": tool_message.tool_call_id if hasattr(tool_message, 'tool_call_id') else None,
                                "raw_content": tool_message.content,
                                "error": "Content is not valid JSON"
                            })
                        except Exception as e:
                            print(f"AgentManager: Error processing tool message content: {e}")
                            tool_outputs.append({
                                "tool_name": tool_message.name,
                                "tool_call_id": tool_message.tool_call_id if hasattr(tool_message, 'tool_call_id') else None,
                                "error": f"Error processing tool message: {str(e)}"
                            })


        final_response_text = "\n".join(formatted_response).strip()
        if not final_response_text: # Ensure there's always some text response
            final_response_text = "Agent processed the request."

        # Print the size of tool_outputs
        # try:
        #     tool_outputs_size = len(json.dumps(tool_outputs))
        #     print(f"\n\n\nAgentManager: Approximate size of tool_outputs: {tool_outputs_size} bytes\n\n\n")
        # except Exception as e:
        #     print(f"\n\n\nAgentManager: Error calculating size of tool_outputs: {e}\n\n\n")
            
        # return {"text_response": final_response_text, "tool_outputs": tool_outputs}
