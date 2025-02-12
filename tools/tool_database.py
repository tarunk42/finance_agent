import json
import os

class ToolDatabase:
    """
    Class to manage tool and function database for agent reasoning.
    """

    def __init__(self, json_path=None):
        """
        Load tools from JSON file.
        """
        # Dynamically determine the correct path
        if json_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Get the 'finance_agent' directory
            json_path = os.path.join(base_dir, "data", "tools_db.json")

        if not os.path.exists(json_path):
            raise FileNotFoundError(f"Tool database not found at {json_path}")

        with open(json_path, "r") as file:
            self.data = json.load(file)

    def get_tools(self):
        """
        Returns all available tools.
        """
        return self.data["tools"]

    def get_tool_by_name(self, tool_name):
        """
        Retrieves tool details by name.
        """
        for tool in self.data["tools"]:
            if tool["name"] == tool_name:
                return tool
        return None

    def get_function_description(self, tool_name, function_name):
        """
        Retrieves function details from a tool.
        """
        tool = self.get_tool_by_name(tool_name)
        if tool and function_name in tool["functions"]:
            return tool["functions"][function_name]
        return None

# Example usage
if __name__ == "__main__":
    db = ToolDatabase()
    print(db.get_tools())  # List all tools
    print(db.get_tool_by_name("StockMarketTool"))  # Get a specific tool
    print(db.get_function_description("StockMarketTool", "get_stock_price"))  # Get function details
