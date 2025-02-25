import os
import sys
import requests
from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool
from typing import Dict, Any

# Get the absolute path of the finance_agents directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
import config
# print(f"API Key: {config.EXCHANGE_RATE_API_KEY}")

class CurrencyExchangeInput(BaseModel):
    from_currency: str = Field(description="Currency code to convert from (e.g., USD, EUR, GBP).")
    to_currency: str = Field(description="Currency code to convert to (e.g., JPY, INR, CAD).")
    amount: float = Field(description="Amount to convert.")

class CurrencyExchangeTool(BaseTool):
    name: str = "currency_exchange_tool"
    description: str = "Fetches real-time currency exchange rates and performs conversions."
    api_key: str = config.EXCHANGE_RATE_API_KEY
    base_url: str = "https://v6.exchangerate-api.com/v6/"  # ExchangeRate-API
    ecb_url: str = "https://api.exchangeratesapi.io/latest"  # ECB API fallback
    
    def _fetch_exchange_rate(self, from_currency: str, to_currency: str) -> float:
        """Fetches exchange rate from ExchangeRate-API, falls back to ECB API if needed."""
        try:
            url = f"{self.base_url}{self.api_key}/latest/{from_currency}"
            response = requests.get(url)
            data = response.json()
            
            if response.status_code == 200 and "conversion_rates" in data:
                return data["conversion_rates"].get(to_currency, None)
        except Exception:
            pass  # If API fails, use fallback
        
        # Fallback to ECB API (EUR-based rates)
        try:
            response = requests.get(self.ecb_url)
            data = response.json()
            if "rates" in data and from_currency in data["rates"] and to_currency in data["rates"]:
                return data["rates"][to_currency] / data["rates"][from_currency]
        except Exception:
            pass
        
        return None  # Failed both APIs
    
    def _convert_currency(self, from_currency: str, to_currency: str, amount: float) -> Dict[str, Any]:
        """Performs currency conversion."""
        rate = self._fetch_exchange_rate(from_currency, to_currency)
        if rate:
            return {
                "from_currency": from_currency,
                "to_currency": to_currency,
                "amount": amount,
                "converted_amount": round(amount * rate, 2),
                "exchange_rate": rate
            }
        return {"error": "Failed to fetch exchange rate."}
    
    def _run(self, from_currency: str, to_currency: str, amount: float) -> Dict[str, Any]:
        return self._convert_currency(from_currency, to_currency, amount)
    
    async def _arun(self, from_currency: str, to_currency: str, amount: float) -> Dict[str, Any]:
        return self._convert_currency(from_currency, to_currency, amount)


# currency_exchange_tool = CurrencyExchangeTool()
# print(currency_exchange_tool._run(from_currency="USD", to_currency="INR", amount=100))