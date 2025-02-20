from transformers import pipeline
from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool
from typing import Type, Any, Dict

class SentimentAnalysisInput(BaseModel):
    text: str = Field(description="Financial news headline or tweet for sentiment analysis.")

class SentimentAnalysisTool(BaseTool):
    name: str = "sentiment_analysis"
    description: str = "Analyzes sentiment of financial text (news headlines, tweets)."
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        object.__setattr__(self, "model", pipeline("text-classification", model="ProsusAI/finbert"))
    
    def _analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Analyzes sentiment of the given text."""
        try:
            result = self.model(text)[0]  # Get first prediction
            return {
                "text": text,
                "sentiment": result["label"],
                "confidence": round(result["score"], 2)
            }
        except Exception as e:
            return {"error": f"Sentiment analysis failed: {str(e)}"}
    
    def _run(self, text: str) -> Dict[str, Any]:
        """Synchronous sentiment analysis."""
        return self._analyze_sentiment(text)
    
    async def _arun(self, text: str) -> Dict[str, Any]:
        """Asynchronous sentiment analysis."""
        return self._analyze_sentiment(text)
    



