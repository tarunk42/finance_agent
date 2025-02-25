import requests
from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool
from typing import Dict, Any
import os
import sys

# Get the absolute path of the finance_agents directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
import config

class SearchInput(BaseModel):
    query: str = Field(description="Search query string.")
    num_results: int = Field(default=5, description="Number of search results to return.")

class SearchTool(BaseTool):
    name: str = "search_tool"
    description: str = "Performs a web search using SerperAPI."
    api_key: str = config.SERPER_API_KEY
    base_url: str = "https://google.serper.dev/search"
    
    def _perform_search(self, query: str, num_results: int) -> Dict[str, Any]:
        """Fetches search results from SerperAPI."""
        headers = {"X-API-KEY": self.api_key, "Content-Type": "application/json"}
        payload = {"q": query, "num": num_results}
        
        try:
            response = requests.post(self.base_url, json=payload, headers=headers)
            data = response.json()
            
            if "organic" in data:
                results = [
                    {"title": entry["title"], "link": entry["link"], "snippet": entry.get("snippet", "")}
                    for entry in data["organic"][:num_results]
                ]
                return {"query": query, "results": results}
            else:
                return {"error": "No results found"}
        except Exception as e:
            return {"error": str(e)}
    
    def _run(self, query: str, num_results: int = 5) -> Dict[str, Any]:
        return self._perform_search(query, num_results)
    
    async def _arun(self, query: str, num_results: int = 5) -> Dict[str, Any]:
        return self._perform_search(query, num_results)



# search_tool = SearchTool()
# print(search_tool._run(query="esp32 s3 wroom buy", num_results=3))