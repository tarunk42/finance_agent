import os
from dotenv import load_dotenv, find_dotenv

# Load environment variables
load_dotenv(find_dotenv())

# API Keys
SERPER_API_KEY = os.getenv("SERPER_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPEN_WEATHER_API_KEY = os.getenv("OPEN_WEATHER_API_KEY")
SERP_API_KEY = os.getenv("SERP_API_KEY")
FMP_API_KEY = os.getenv("FMP_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# OpenAI Model Selection
OPENAI_MODEL = 'gpt-4o-mini'

# System Prompt
SYSTEM_PROMPTS = {
    "financial_assistant": """You are a financial assistant specialized in stock market insights, trend analysis, 
    financial news, and sentiment analysis. 

    **Instructions:**
    - **Always use the appropriate tools before answering.**  
    - If asked about stock prices, call `StockMarketTool`.  
    - If asked about financial news, call `NewsAPITool`.  
    - If unsure, ask the user for clarification **instead of assuming**.  
    - Do NOT provide generic responses like "I cannot access real-time data". **Always attempt to fetch data first**.

    **Example Usage:**
    - User: "What’s Tesla’s stock price today?"  
      - ✅ Correct: Call `StockMarketTool("TSLA")`  
      - ❌ Wrong: "I cannot access real-time stock prices."
    
    Think step by step before responding.
    """
}


# Tool Registry (List of tools to be loaded dynamically)
TOOL_REGISTRY = [
    "StockMarketTool",
    "HistoricalStockMarketTool",
    "TrendAnalysisTool",
    "NewsAPITool",
    "SentimentAnalysisTool",
    "CryptoMarketTool",
]
