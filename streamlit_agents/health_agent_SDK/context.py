from pydantic import BaseModel
from typing import Optional, List, Dict
from agents import RunContextWrapper

class UserSessionContext(BaseModel):
    name: str
    uid: int
    goal: Optional[dict] = None
    diet_preferences: Optional[str] = None
    workout_plan: Optional[dict] = None
    meal_plan: Optional[List[str]] = None
    injury_notes: Optional[str] = None
    handoff_logs: List[str] = []
    progress_logs: List[Dict[str, str]] = []
    history: List[str] = []

def get_user_context(name, uid):
    return RunContextWrapper(context=UserSessionContext(name=name, uid=uid))