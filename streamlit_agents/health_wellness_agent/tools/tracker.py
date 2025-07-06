"""
Progress Tracker Tool - Manages and evaluates user fitness progress updates.
"""

from typing import Dict, Any, List
from datetime import datetime
from context import RunContextWrapper
from hooks import hook_manager

class ProgressTrackerTool:
    """
    Tool responsible for validating, logging, analyzing progress,
    and providing tailored recommendations.
    """

    def __init__(self):
        self.name = "progress_tracker"

    def record_progress(self, progress_input: Dict[str, Any], context_wrapper: RunContextWrapper) -> Dict[str, Any]:
        """
        Validates incoming progress data, updates user session context,
        analyzes current progress, and returns insights with recommendations.
        """
        hook_manager.log_tool_start(self.name)

        try:
            # Step 1: Validate incoming progress data
            sanitized_data = self._validate_progress_data(progress_input)

            # Step 2: Log the progress update into the context
            self._log_progress_to_context(sanitized_data, context_wrapper)

            # Step 3: Perform analysis on the progress data
            progress_analysis = self._analyze_progress_metrics(sanitized_data)

            # Step 4: Generate actionable recommendations based on analysis
            recs = self._generate_recommendations(progress_analysis)

            return {
                "response_type": "progress_update",
                "content": {
                    "message": "Your progress has been recorded successfully!",
                    "progress_data": sanitized_data,
                    "analysis": progress_analysis,
                    "recommendations": recs
                }
            }

        except Exception as err:
            return {
                "response_type": "error",
                "content": {"error": f"Progress update failed: {str(err)}"}
            }

    def _validate_progress_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sanitizes and structures the raw progress input data.
        Ensures numeric conversion and timestamps the update.
        """
        validated = {
            "timestamp": datetime.now().isoformat(),
            "notes": data.get("notes", "").strip(),
            "metrics": {}
        }

        if "weight" in data:
            validated["metrics"]["weight"] = float(data["weight"])

        if "workouts_completed" in data:
            validated["metrics"]["workouts_completed"] = int(data["workouts_completed"])

        return validated

    def _log_progress_to_context(self, progress_data: Dict[str, Any], context_wrapper: RunContextWrapper):
        """
        Logs progress data into the user session's progress log for historical tracking.
        """
        import json
        context_wrapper.get_context().add_progress_log("progress_update", json.dumps(progress_data))

    def _analyze_progress_metrics(self, progress_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyzes progress metrics such as workouts completed,
        and generates insightful messages for the user.
        """
        analysis_result = {
            "overall_score": 75,  # Static example score; replace with real logic if needed
            "insights": []
        }

        workouts_done = progress_data.get("metrics", {}).get("workouts_completed", 0)

        if workouts_done >= 3:
            analysis_result["insights"].append("Excellent consistency with workouts!")
        elif workouts_done >= 1:
            analysis_result["insights"].append("Good start! Try to increase workout frequency.")
        else:
            analysis_result["insights"].append("Let's aim for more regular workouts.")

        return analysis_result

    def _generate_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """
        Creates personalized recommendations based on the progress analysis.
        """
        base_recommendations = [
            "Continue tracking your progress consistently.",
            "Maintain dedication to your plan.",
            "Celebrate your small milestones."
        ]

        if analysis.get("overall_score", 100) < 50:
            base_recommendations.append("You might consider adjusting your goals to be more attainable.")

        return base_recommendations
