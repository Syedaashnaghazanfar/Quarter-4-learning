"""
Context Management for Health & Wellness Planner Agent
"""
from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from datetime import datetime

class UserSessionContext(BaseModel):
    """User session context"""
    name: str = ""
    uid: int = 0
    goal: Optional[Dict[str, Any]] = None
    diet_preferences: Optional[str] = None
    workout_plan: Optional[Dict[str, Any]] = None
    meal_plan: Optional[List[str]] = None
    injury_notes: Optional[str] = None
    handoff_logs: List[str] = []
    progress_logs: List[Dict[str, str]] = []
    
    def update_context(self, **kwargs):
        """Update context with new values"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def add_progress_log(self, log_type: str, message: str):
        """Add progress log"""
        self.progress_logs.append({
            "timestamp": datetime.now().isoformat(),
            "type": log_type,
            "message": message
        })
    
    def add_handoff_log(self, message: str):
        """Add handoff log"""
        self.handoff_logs.append(f"{datetime.now().isoformat()}: {message}")

class RunContextWrapper:
    """Context wrapper"""
    
    def __init__(self, context: UserSessionContext):
        self.context = context
    
    def get_context(self) -> UserSessionContext:
        """Get current context"""
        return self.context
    
    def update_context(self, **kwargs):
        """Update context"""
        self.context.update_context(**kwargs)