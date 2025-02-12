import sys
import os
MODEL  = "llama3.2:3b-instruct-q8_0"
# Get the absolute path of the project directory
# project_root = os.path.abspath(os.path.join(os.getcwd(), ".."))

# # Add it to sys.path
# if project_root not in sys.path:
#     sys.path.append(project_root)

import json
import ollama
import re
from tools.stock_market_tool import StockMarketTool
from tools.crypto_market_tool import CryptoMarketTool
from tools.news_api_tool import NewsAPITool
from tools.sentiment_analysis_tool import SentimentAnalysisTool
from tools.trend_analysis_tool import TrendAnalysisTool

class DataRetrievalAgent:
    """
    Data Retrieval Agent using Ollama to process financial queries and call appropriate tools.
    """
    
    def __init__(self):
        self.model = "mistral"
        self.tools = {
            "StockMarketTool": StockMarketTool(),
            "CryptoMarketTool": CryptoMarketTool(),
            "NewsAPITool": NewsAPITool(),
            "SentimentAnalysisTool": SentimentAnalysisTool(),
            "TrendAnalysisTool": TrendAnalysisTool()
        }

    def clean_json_response(self, response_text):
        """
        Cleans response text to remove Markdown formatting and ensure valid JSON.
        """
        response_text = response_text.strip()
        response_text = re.sub(r'```json|```', '', response_text).strip()
        return response_text

    def generate_tool_calls(self, query):
        """
        Uses Ollama to generate structured JSON for tool execution.
        """
        messages = [
            {"role": "system", "content": "You are a financial assistant. Always return a valid JSON object with correct tool names: StockMarketTool, CryptoMarketTool, NewsAPITool, SentimentAnalysisTool, TrendAnalysisTool. Do not include Markdown, explanations, or incorrect tool names. Ensure tool_calls is always populated."},
            {"role": "user", "content": f"User Query: {query}\n\nReturn JSON format like:\n{{\n    \"tool_calls\": [\n        {{ \"tool\": \"StockMarketTool\", \"function\": \"get_stock_price\", \"parameters\": {{ \"ticker\": \"TSLA\" }} }}\n    ]\n}}"}
        ]
        
        response = ollama.chat(model=self.model, messages=messages)
        print("Ollama Raw Response:", response)  # Debugging Line
        
        try:
            json_content = self.clean_json_response(response.message.content)
            parsed_json = json.loads(json_content)
            
            # Validate tool names and ensure tool_calls isn't empty
            valid_tool_calls = []
            for tool_call in parsed_json.get("tool_calls", []):
                if tool_call["tool"] in self.tools:
                    valid_tool_calls.append(tool_call)
            
            if not valid_tool_calls:
                return {"error": "No valid tool calls generated", "raw_response": json_content}
            
            return {"tool_calls": valid_tool_calls}
        except (json.JSONDecodeError, AttributeError, KeyError):
            return {"error": "Invalid JSON response from Ollama", "raw_response": response.message.content}

    def execute_tool_calls(self, tool_calls):
        """
        Executes tool calls and returns structured results.
        """
        results = []
        for call in tool_calls.get("tool_calls", []):
            tool_name = call["tool"]
            function_name = call["function"]
            parameters = call["parameters"]
            
            if tool_name in self.tools:
                tool = self.tools[tool_name]
                function = getattr(tool, function_name, None)
                
                if function:
                    result = function(**parameters)
                    results.append({"tool": tool_name, "output": result})
                else:
                    results.append({"tool": tool_name, "error": f"Function {function_name} not found"})
            else:
                results.append({"tool": tool_name, "error": "Tool not recognized"})
        
        return {"results": results}

    def process_query(self, query):
        """
        Main function to handle user queries.
        """
        tool_calls = self.generate_tool_calls(query)
        if "error" in tool_calls:
            return tool_calls
        
        return self.execute_tool_calls(tool_calls)

# Example usage
if __name__ == "__main__":
    agent = DataRetrievalAgent()
    query = "Get Tesla's stock price today."
    result = agent.process_query(query)
    print(json.dumps(result, indent=4))
