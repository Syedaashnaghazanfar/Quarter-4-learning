"""
Escalation Agent - Human Coach ko involve karne wala module
Yeh agent tab activate hota hai jab user ko human assistance chahiye hoti hai
"""

from typing import Dict, Any
from context import RunContextWrapper
from hooks import hook_manager

class EscalationAgent:
    def __init__(self):
        self.name = "escalation_agent"

    def handle_escalation(self, context: RunContextWrapper, reason: str = "general") -> Dict[str, Any]:
        """
        Jab user ko help chahiye hoti hai, toh yeh method human coach ko connect karta hai
        """

        # Handoff ka log maintain kiya ja raha hai taake tracking ho sake
        hook_manager.log_handoff("main_agent", self.name)

        # User context mein handoff ka entry add kiya gaya hai
        context.get_context().add_handoff_log(f"Escalated to human coach: {reason}")

        # User ki summary tayar ki ja rahi hai jo human coach ko bheji jaayegi
        user_summary = self.prepare_user_summary(context)

        # Human coach ko connect karne ka message return hota hai
        return {
            "response_type": "escalation",
            "content": {
                "message": "Main aapko ek human coach se connect kar raha hoon.",
                "escalation_reason": reason,
                "user_summary": user_summary,
                "next_steps": [
                    "Aapka request hamare coaching team ko bhej diya gaya hai.",
                    "Ek certified trainer aap se 24 ghanton ke andar raabta karega.",
                    "Aap is dauraan app ka istemal jaari rakh sakte hain."
                ],
                "estimated_wait_time": "24 hours"
            }
        }

    def prepare_user_summary(self, context: RunContextWrapper) -> Dict[str, Any]:
        """
        Yeh method user ka context le kar ek summary banata hai jo human coach ko samajhne mein madad karti hai
        """

        user_context = context.get_context()

        return {
            "user_name": user_context.name,
            "primary_goal": user_context.goal,
            "dietary_preferences": user_context.diet_preferences,
            "workout_plan": user_context.workout_plan,
            "progress_entries": len(user_context.progress_logs)
        }
