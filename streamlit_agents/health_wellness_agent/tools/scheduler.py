"""
Check-in Scheduler Tool - Manages and automates user progress check-ins.
"""

from typing import Dict, Any, List
from datetime import datetime, timedelta
from context import RunContextWrapper
from hooks import hook_manager

class CheckingSchedulerTool:
    """
    Tool responsible for scheduling periodic user check-ins and providing structured prompts.
    """

    def __init__(self):
        self.name = "checkin_scheduler"

    def initiate_checkin_schedule(self, frequency_text: str, context_wrapper: RunContextWrapper) -> Dict[str, Any]:
        """
        Schedules future check-in dates based on user-selected frequency and updates session context.
        """
        hook_manager.log_tool_start(self.name)

        try:
            # Convert text input into day-interval
            days_interval = self._frequency_to_days(frequency_text)

            # Build the full check-in schedule with questions
            checkin_plan = self._build_checkin_plan(days_interval, context_wrapper)

            # Log progress
            context_wrapper.get_context().add_progress_log(
                "checkin_scheduling", f"Scheduled check-ins: {frequency_text}"
            )

            return {
                "response_type": "schedule",
                "content": {
                    "message": f"Check-ins successfully scheduled ({frequency_text}).",
                    "schedule": checkin_plan,
                    "next_checkin": checkin_plan["next_checkin"]
                }
            }

        except Exception as e:
            return {
                "response_type": "error",
                "content": {"error": f"Failed to schedule check-ins: {str(e)}"}
            }

    def _frequency_to_days(self, frequency: str) -> int:
        """
        Converts natural language frequency to numeric day interval.
        Defaults to weekly if not recognized.
        """
        freq = frequency.strip().lower()
        if "daily" in freq:
            return 1
        elif "weekly" in freq:
            return 7
        elif "biweekly" in freq:
            return 14
        return 7  # fallback default

    def _build_checkin_plan(self, interval_days: int, context: RunContextWrapper) -> Dict[str, Any]:
        """
        Builds check-in schedule and generates relevant reflection questions.
        """
        today = datetime.now()
        checkin_dates = []

        # Generate four upcoming check-in dates
        for i in range(4):
            upcoming_date = today + timedelta(days=interval_days * (i + 1))
            checkin_dates.append({
                "date": upcoming_date.strftime("%Y-%m-%d"),
                "day": upcoming_date.strftime("%A")
            })

        # Generate dynamic questions
        question_set = self._generate_checkin_questions(context)

        return {
            "frequency_days": interval_days,
            "next_checkin": checkin_dates[0],
            "upcoming_checkins": checkin_dates,
            "questions": question_set
        }

    def _generate_checkin_questions(self, context: RunContextWrapper) -> List[str]:
        """
        Returns a base set of questions, enhanced with goal-specific items.
        """
        questions = [
            "How do you feel about your progress so far?",
            "Were you able to stick to your nutrition plan?",
            "How many workouts did you complete since the last check-in?",
            "What roadblocks or challenges did you face?",
            "What are you proud of this week?"
        ]

        # Add goal-specific questions
        user_goal = context.get_context().goal
        if user_goal and isinstance(user_goal, dict):
            if user_goal.get('goal_type') == 'weight_loss':
                questions.append("Have you recorded your current weight?")

        return questions
