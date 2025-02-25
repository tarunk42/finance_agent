from datetime import datetime, timedelta
from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool
from typing import Dict, Any

class DateTimeInput(BaseModel):
    days_offset: int = Field(default=0, description="Days offset from today. Use negative for past dates, positive for future dates.")
    format: str = Field(default="%Y-%m-%d %H:%M:%S", description="Datetime format string (default: ISO format).")

class DateTimeTool(BaseTool):
    name: str = "datetime_tool"
    description: str = "Provides current or offset date and time."
    
    def _get_datetime(self, days_offset: int, format: str) -> Dict[str, Any]:
        """Fetches the current or offset datetime."""
        target_date = datetime.now() + timedelta(days=days_offset)
        return {
            "requested_offset_days": days_offset,
            "datetime": target_date.strftime(format)
        }
    
    def _run(self, days_offset: int = 0, format: str = "%Y-%m-%d %H:%M:%S") -> Dict[str, Any]:
        return self._get_datetime(days_offset, format)
    
    async def _arun(self, days_offset: int = 0, format: str = "%Y-%m-%d %H:%M:%S") -> Dict[str, Any]:
        return self._get_datetime(days_offset, format)


# datetime_tool = DateTimeTool()
# print(datetime_tool._run(days_offset=-30))
