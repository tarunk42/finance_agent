import os
import sys
import requests
from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool
from typing import Dict, Any, Optional
from datetime import datetime, timezone

# Get the absolute path of the finance_agents directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
import config

class WeatherInput(BaseModel):
    location: str = Field(description="City name, optionally with country code (e.g., 'London, UK', 'Paris, FR').")
    lat: Optional[float] = Field(default=None, description="Latitude for precise location.")
    lon: Optional[float] = Field(default=None, description="Longitude for precise location.")
    unit: str = Field(default="metric", description="Temperature unit: 'metric' (°C) or 'imperial' (°F).")

class WeatherTool(BaseTool):
    name: str = "weather_tool"
    description: str = "Fetches real-time weather data using OpenWeather API."
    api_key: str = config.OPEN_WEATHER_API_KEY
    base_url: str = "https://api.openweathermap.org/data/2.5/weather"
    
    def _fetch_weather(self, location: str, lat: Optional[float], lon: Optional[float], unit: str) -> Dict[str, Any]:
        """Fetches weather data from OpenWeather API with improved location handling."""
        params = {"appid": self.api_key, "units": unit}
        
        if lat is not None and lon is not None:
            params.update({"lat": lat, "lon": lon})
        else:
            params.update({"q": location})
        
        try:
            response = requests.get(self.base_url, params=params)
            data = response.json()
            
            if response.status_code == 200:
                sunrise = datetime.fromtimestamp(data["sys"].get("sunrise"), timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
                sunset = datetime.fromtimestamp(data["sys"].get("sunset"), timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
                return {
                    "location": f"{data.get('name')}, {data.get('sys', {}).get('country', '')}",
                    "temperature": data["main"].get("temp"),
                    "feels_like": data["main"].get("feels_like"),
                    "humidity": data["main"].get("humidity"),
                    "pressure": data["main"].get("pressure"),
                    "weather": data["weather"][0].get("description"),
                    "wind_speed": data["wind"].get("speed"),
                    "visibility": data.get("visibility", "N/A"),
                    "sunrise": sunrise,
                    "sunset": sunset
                }
            elif response.status_code == 404:
                return {"error": "Location not found. Please specify a country code or use latitude/longitude."}
            return {"error": data.get("message", "Failed to fetch weather data.")}
        except Exception as e:
            return {"error": str(e)}
    
    def _run(self, location: str, lat: Optional[float] = None, lon: Optional[float] = None, unit: str = "metric") -> Dict[str, Any]:
        return self._fetch_weather(location, lat, lon, unit)
    
    async def _arun(self, location: str, lat: Optional[float] = None, lon: Optional[float] = None, unit: str = "metric") -> Dict[str, Any]:
        return self._fetch_weather(location, lat, lon, unit)




# weather_tool = WeatherTool()
# print(weather_tool._run("New York", unit="imperial"))  # Example usage