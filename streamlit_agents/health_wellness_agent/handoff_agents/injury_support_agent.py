"""
Injury Support Agent - Provides personalized recommendations and safe workout plans for users with injuries.
"""

from typing import Dict, Any, List
from context import RunContextWrapper
from hooks import hook_manager

class InjurySupportAgent:
    """Agent to assist users who report an injury, offering safe alternatives and suggestions."""

    def __init__(self):
        self.name = "injury_support_agent"

    def handle_injury_consultation(self, context: RunContextWrapper, injury_type: str = "general") -> Dict[str, Any]:
        """
        Handles the injury consultation by analyzing the injury, providing guidance,
        and generating a modified workout plan suitable for recovery.
        """

        # Track the escalation from main agent to injury support
        hook_manager.log_handoff("main_agent", self.name)

        # Log the injury report in the user's session context
        context.get_context().add_handoff_log(f"Injury reported: {injury_type}")

        # Perform injury-specific analysis
        injury_analysis = self._analyze_injury(injury_type)
        recommendations = self._generate_recommendations(injury_type)
        modified_workout = self._create_modified_workout(injury_type)

        # Store summary in the session for tracking
        context.update_context(injury_notes=f"Injury: {injury_type} | Recovery plan generated")

        return {
            "response_type": "injury_consultation",
            "content": {
                "message": "I've created a safe exercise plan based on your injury.",
                "injury_type": injury_type,
                "injury_analysis": injury_analysis,
                "recommendations": recommendations,
                "modified_workout_plan": modified_workout,
                "safety_guidelines": self._get_safety_guidelines(injury_type)
            }
        }

    def _analyze_injury(self, injury_type: str) -> Dict[str, Any]:
        """
        Analyzes the reported injury and returns affected areas, safe and unsafe movements.
        """
        analysis = {
            "injury_type": injury_type,
            "severity": "moderate",
            "affected_areas": [],
            "safe_movements": [],
            "avoid_movements": []
        }

        if injury_type == "knee":
            analysis.update({
                "affected_areas": ["knee", "lower leg"],
                "safe_movements": ["swimming", "upper body exercises"],
                "avoid_movements": ["running", "jumping", "deep squats"]
            })
        elif injury_type == "back":
            analysis.update({
                "affected_areas": ["lower back", "core"],
                "safe_movements": ["light walking", "gentle stretching"],
                "avoid_movements": ["lifting weights", "twisting motions"]
            })
        elif injury_type == "shoulder":
            analysis.update({
                "affected_areas": ["shoulder", "upper arm"],
                "safe_movements": ["leg workouts", "cardio walking"],
                "avoid_movements": ["overhead lifts", "heavy pushing"]
            })

        return analysis

    def _generate_recommendations(self, injury_type: str) -> List[Dict[str, Any]]:
        """
        Returns a list of recovery and safety recommendations based on the injury type.
        """
        tips = [
            {
                "category": "Precaution",
                "priority": "high",
                "recommendation": "Stop exercising immediately if pain increases.",
                "reason": "To prevent further injury."
            },
            {
                "category": "Recovery",
                "priority": "high",
                "recommendation": "Apply ice after activity if swelling occurs.",
                "reason": "To reduce inflammation."
            }
        ]

        if injury_type == "knee":
            tips.append({
                "category": "Workout Modification",
                "priority": "medium",
                "recommendation": "Focus on upper body or aquatic exercises.",
                "reason": "To avoid stress on the injured knee."
            })

        return tips

    def _create_modified_workout(self, injury_type: str) -> Dict[str, Any]:
        """
        Creates a modified weekly workout plan that is safe based on the user's injury.
        """
        if injury_type == "knee":
            return {
                "weekly_plan": [
                    {"day": "Monday", "focus": "Upper Body", "exercises": ["Seated Shoulder Press", "Chest Press", "Seated Row"], "notes": "Perform seated exercises only."},
                    {"day": "Wednesday", "focus": "Core + Stretching", "exercises": ["Seated Twists", "Arm Raises"], "notes": "Keep all movements controlled and stable."},
                    {"day": "Friday", "focus": "Cardio", "exercises": ["Swimming", "Water Jogging"], "notes": "Low-impact, water-based activities recommended."}
                ]
            }
        elif injury_type == "back":
            return {
                "weekly_plan": [
                    {"day": "Monday", "focus": "Mobility", "exercises": ["Walking", "Gentle Stretching"], "notes": "Avoid bending or heavy lifting."},
                    {"day": "Wednesday", "focus": "Core Stability", "exercises": ["Bird Dog", "Wall Plank"], "notes": "Focus on posture and alignment."},
                    {"day": "Friday", "focus": "Lower Body (Modified)", "exercises": ["Glute Bridge", "Heel Slides"], "notes": "Use a mat and avoid pressure on spine."}
                ]
            }
        else:
            return {
                "weekly_plan": [
                    {"day": "Monday", "focus": "Lower Body (Isolated)", "exercises": ["Wall Sit", "Leg Raises"], "notes": "Skip exercises that cause pain."},
                    {"day": "Wednesday", "focus": "Light Cardio", "exercises": ["Stationary Bike", "Walking"], "notes": "Stick to low-impact sessions."},
                    {"day": "Friday", "focus": "Stretching", "exercises": ["Yoga Stretches", "Foam Rolling"], "notes": "Emphasize slow, relaxing movements."}
                ]
            }

    def _get_safety_guidelines(self, injury_type: str) -> List[str]:
        """
        Provides general safety tips to prevent aggravating the injury.
        """
        tips = [
            "Start slowly and gradually increase intensity.",
            "Stop immediately if you feel sharp or persistent pain.",
            "Avoid high-impact or risky movements unless cleared by a doctor."
        ]

        if injury_type == "knee":
            tips.append("Avoid exercises that involve deep bending or jumping.")
        elif injury_type == "back":
            tips.append("Maintain a neutral spine position at all times.")

        return tips
