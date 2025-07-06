"""
FitnessPlanner – Personalized Workout Assistant
"""

from typing import Dict, Any
from context import RunContextWrapper
from guardrails import GuardrailValidator
from hooks import hook_manager

class WorkoutRecommenderTool:
    """Smart assistant for curating weekly workout routines based on goals and preferences."""

    def __init__(self):
        self.name = "fitness_planner"

    def generate_plan(self, user_input: str, goal: Dict[str, Any], context: RunContextWrapper) -> Dict[str, Any]:
        """Crafts a customized weekly fitness schedule."""
        hook_manager.log_tool_start(self.name)

        try:
            profile = self._analyze_preferences(user_input)
            schedule = self._build_weekly_schedule(profile, goal)

            context.update_context(workout_plan=schedule)
            context.get_context().add_progress_log("fitness_planner", "Workout routine generated.")

            result = {
                "response_type": "fitness_plan",
                "content": schedule
            }

            return GuardrailValidator.validate_output(result)

        except Exception as err:
            return {
                "response_type": "error",
                "content": {"error": str(err)}
            }

    def _analyze_preferences(self, input_text: str) -> Dict[str, Any]:
        """Interprets fitness level and workout style from user description."""
        experience = "beginner"
        workout_style = "strength"

        input_text = input_text.lower()

        if "advanced" in input_text or "expert" in input_text:
            experience = "advanced"
        elif "intermediate" in input_text:
            experience = "intermediate"

        if "cardio" in input_text:
            workout_style = "cardio"

        return {
            "level": experience,
            "style": workout_style
        }

    def _build_weekly_schedule(self, profile: Dict[str, Any], goal: Dict[str, Any]) -> Dict[str, Any]:
        """Generates a weekly workout routine based on user profile and fitness goal."""

        strength_routines = {
            "beginner": [
                {"day": "Monday", "focus": "Upper Body", "exercises": ["Push-ups", "Pull-ups", "Shoulder Press"], "duration": "30 min"},
                {"day": "Wednesday", "focus": "Lower Body", "exercises": ["Squats", "Lunges", "Calf Raises"], "duration": "30 min"},
                {"day": "Friday", "focus": "Full Body", "exercises": ["Burpees", "Planks", "Mountain Climbers"], "duration": "30 min"},
            ],
            "intermediate": [
                {"day": "Monday", "focus": "Chest & Triceps", "exercises": ["Bench Press", "Dips", "Tricep Extensions"], "duration": "45 min"},
                {"day": "Tuesday", "focus": "Back & Biceps", "exercises": ["Rows", "Pull-ups", "Bicep Curls"], "duration": "45 min"},
                {"day": "Thursday", "focus": "Legs", "exercises": ["Squats", "Deadlifts", "Lunges"], "duration": "45 min"},
                {"day": "Friday", "focus": "Shoulders", "exercises": ["Shoulder Press", "Lateral Raises", "Shrugs"], "duration": "45 min"},
            ],
            "advanced": [
                {"day": "Monday", "focus": "Chest", "exercises": ["Bench Press", "Incline Press", "Flyes"], "duration": "60 min"},
                {"day": "Tuesday", "focus": "Back", "exercises": ["Deadlifts", "Rows", "Pull-ups"], "duration": "60 min"},
                {"day": "Wednesday", "focus": "Legs", "exercises": ["Squats", "RDLs", "Leg Press"], "duration": "60 min"},
                {"day": "Thursday", "focus": "Shoulders", "exercises": ["Military Press", "Lateral Raises", "Rear Delts"], "duration": "60 min"},
                {"day": "Friday", "focus": "Arms", "exercises": ["Close-Grip Bench", "Tricep Dips", "Bicep Curls"], "duration": "60 min"},
            ]
        }

        cardio_routines = {
            "beginner": [
                {"day": "Monday", "activity": "Walking", "duration": "20 min"},
                {"day": "Wednesday", "activity": "Cycling", "duration": "15 min"},
                {"day": "Friday", "activity": "Swimming", "duration": "15 min"},
            ],
            "intermediate": [
                {"day": "Monday", "activity": "Running", "duration": "30 min"},
                {"day": "Tuesday", "activity": "HIIT", "duration": "25 min"},
                {"day": "Thursday", "activity": "Cycling", "duration": "35 min"},
                {"day": "Saturday", "activity": "Long Walk", "duration": "45 min"},
            ],
            "advanced": [
                {"day": "Monday", "activity": "Interval Running", "duration": "40 min"},
                {"day": "Tuesday", "activity": "HIIT Circuit", "duration": "30 min"},
                {"day": "Wednesday", "activity": "Cycling", "duration": "50 min"},
                {"day": "Thursday", "activity": "Swimming", "duration": "40 min"},
                {"day": "Saturday", "activity": "Long Run", "duration": "60 min"},
            ]
        }

        chosen_type = profile["style"]
        level = profile["level"]

        plan = cardio_routines[level] if chosen_type == "cardio" else strength_routines[level]

        return {
            "plan_type": chosen_type,
            "fitness_level": level,
            "weekly_schedule": plan,
            "reminders": [
                "Start each session with a warm-up 🌟",
                "Hydration is key 💧",
                "Form matters more than reps 🧘",
                "Rest is part of progress 💤"
            ]
        }
