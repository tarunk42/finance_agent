import wikipedia
from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool
from typing import Dict, Any

class WikipediaInput(BaseModel):
    query: str = Field(description="Search query for Wikipedia.")
    sentences: int = Field(default=2, description="Number of summary sentences to return.")

class WikipediaTool(BaseTool):
    name: str = "wikipedia_tool"
    description: str = "Fetches a summary from Wikipedia based on a given query."
    
    def _fetch_wikipedia_summary(self, query: str, sentences: int) -> Dict[str, Any]:
        """Fetches a Wikipedia summary for a given query."""
        try:
            summary = wikipedia.summary(query, sentences=sentences)
            return {"query": query, "summary": summary}
        except wikipedia.exceptions.DisambiguationError as e:
            return {"error": "Disambiguation error", "options": e.options}
        except wikipedia.exceptions.PageError:
            return {"error": "Page not found"}
        except Exception as e:
            return {"error": str(e)}
    
    def _run(self, query: str, sentences: int = 2) -> Dict[str, Any]:
        return self._fetch_wikipedia_summary(query, sentences)
    
    async def _arun(self, query: str, sentences: int = 2) -> Dict[str, Any]:
        return self._fetch_wikipedia_summary(query, sentences)


# wikipedia_tool = WikipediaTool()
# print(wikipedia_tool._run(query="Department of Government Efficiency", sentences=10))