import pytz
from datetime import datetime
from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool
from typing import Dict, Any

class TimeZoneInput(BaseModel):
    timezone: str = Field(description="Timezone string (e.g., 'America/New_York', 'UTC', 'Asia/Tokyo').")
    format: str = Field(default="%Y-%m-%d %H:%M:%S", description="Datetime format string.")

class TimeZoneTool(BaseTool):
    name: str = "timezone_tool"
    description: str = "Fetches the current time for a specified timezone."
    
    def _get_time_in_timezone(self, timezone: str, format: str) -> Dict[str, Any]:
        """Fetches the current time in a given timezone."""
        try:
            tz = pytz.timezone(timezone)
            current_time = datetime.now(tz).strftime(format)
            return {
                "timezone": timezone,
                "current_time": current_time
            }
        except Exception as e:
            return {"error": str(e)}
    
    def _run(self, timezone: str, format: str = "%Y-%m-%d %H:%M:%S") -> Dict[str, Any]:
        return self._get_time_in_timezone(timezone, format)
    
    async def _arun(self, timezone: str, format: str = "%Y-%m-%d %H:%M:%S") -> Dict[str, Any]:
        return self._get_time_in_timezone(timezone, format)


# timezone_tool = TimeZoneTool()
# print(timezone_tool._run(timezone="America/New_York"))