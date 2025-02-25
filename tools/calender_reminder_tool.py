from tinydb import TinyDB, Query
from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool
from typing import Dict, Any, List
import os

# Define database path
data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../data")
os.makedirs(data_dir, exist_ok=True)
db_path = os.path.join(data_dir, "calendar_reminders.json")
db = TinyDB(db_path)

class ReminderInput(BaseModel):
    event: str = Field(description="Event name or title.")
    date: str = Field(description="Date of the event in YYYY-MM-DD format.")
    time: str = Field(description="Time of the event in HH:MM format.")
    description: str = Field(default="", description="Optional event description.")

class CalendarReminderTool(BaseTool):
    name: str = "calendar_reminder_tool"
    description: str = "Stores, retrieves, and manages reminders. Use this tool to check your schedule or manage reminders. You can add, get, or delete reminders."
    
    def _add_reminder(self, event: str, date: str, time: str, description: str) -> Dict[str, Any]:
        """Adds a new reminder."""
        db.insert({"event": event, "date": date, "time": time, "description": description})
        return {"message": "Reminder added successfully."}
    
    def _get_reminders(self, date: str = None) -> List[Dict[str, Any]]:
        """Fetches reminders for a specific date or all upcoming reminders."""
        if date:
            return db.search(Query().date == date)
        return db.all()
    
    def _delete_reminder(self, event: str, date: str) -> Dict[str, Any]:
        """Deletes a specific reminder."""
        db.remove((Query().event == event) & (Query().date == date))
        return {"message": "Reminder deleted successfully."}
    
    def _run(self, action: str, event: str = "", date: str = "", time: str = "", description: str = "") -> Any:
        if action == "add":
            return self._add_reminder(event, date, time, description)
        elif action == "get":
            return self._get_reminders(date)
        elif action == "delete":
            return self._delete_reminder(event, date)
        return {"error": "Invalid action specified."}
    
    async def _arun(self, action: str, event: str = "", date: str = "", time: str = "", description: str = "") -> Any:
        return self._run(action, event, date, time, description)


# calrender_reminder_tool = CalendarReminderTool()
# # add a reminder
# # calrender_reminder_tool._run("add", event="Meeting", date="2025-02-28", time="14:30", description="Team Eating")
# # get all reminders
# print(calrender_reminder_tool._run("get"))
# # delete a reminder
# calrender_reminder_tool._run("delete", event="Meeting", date="2022-12-25")
# print(calrender_reminder_tool._run("get"))