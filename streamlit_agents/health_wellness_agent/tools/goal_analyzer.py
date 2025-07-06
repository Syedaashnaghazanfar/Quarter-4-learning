"""
Goal Analyzer Tool - Parses and evaluates a user's health or wellness goal.
"""

from typing import Dict, Any
from context import RunContextWrapper
from guardrails import GuardrailValidator
from hooks import hook_manager

class GoalAnalyzerTool:
    """
    Evaluates the user's goal, determines feasibility, and returns helpful recommendations.
    """

    def __init__(self):
        self.name = "goal_analyzer"

    def process_user_goal(self, goal_text: str, context_wrapper: RunContextWrapper) -> Dict[str, Any]:
        """
        Entry point for goal analysis. Validates input, updates context, and returns analysis.
        """
        hook_manager.log_tool_start(self.name)

        try:
            # Step 1: Validate the raw goal input
            parsed_goal = GuardrailValidator.validate_goal_input(goal_text)

            # Step 2: Fallback to basic structure if parsing fails
            if not isinstance(parsed_goal, dict):
                parsed_goal = {"original_text": goal_text}

            # Step 3: Update session context with the parsed goal
            context_wrapper.update_context(goal=parsed_goal)
            context_wrapper.get_context().add_progress_log("goal_analysis", f"User goal: {goal_text}")

            # Step 4: Evaluate goal feasibility
            feasibility_summary = self._evaluate_feasibility(parsed_goal)

            # Step 5: Build structured response
            feedback = {
                "response_type": "goal_analysis",
                "content": {
                    "message": f"Thanks! I've reviewed your goal: '{goal_text}'",
                    "goal_data": parsed_goal,
                    "feasibility": feasibility_summary,
                    "recommendations": [
                        "Start with small, consistent changes",
                        "Track your progress weekly or biweekly",
                        "Keep hydration and sleep in check—they matter more than you think"
                    ]
                }
            }

            return GuardrailValidator.validate_output(feedback)

        except Exception as e:
            return {
                "response_type": "error",
                "content": {"error": f"Goal analysis failed: {str(e)}"}
            }

    def _evaluate_feasibility(self, goal_info: Dict[str, Any]) -> str:
        """
        Determine how realistic the user’s goal is based on goal type and numeric value.
        """
        goal_type = goal_info.get('goal_type')
        quantity = goal_info.get('quantity')

        if goal_type == 'weight_loss':
            if quantity and quantity > 2:
                return "Challenging but doable with effort"
            return "Highly achievable with consistency"
        
        elif goal_type == 'exercise':
            if quantity and quantity > 5:
                return "Ambitious but possible with dedication"
            return "Achievable with a structured routine"
        elif goal_type == 'nutrition':
            if quantity and quantity > 3:
                return "Requires significant lifestyle changes"
            return "Achievable with gradual dietary adjustments"
        elif goal_type == 'mental_health':
            if quantity and quantity > 30:
                return "Requires ongoing commitment and support"
            return "Achievable with consistent self-care practices"
        elif goal_type == 'sleep':
            if quantity and quantity < 6:
                return "Needs improvement in sleep hygiene"
            return "Achievable with better sleep habits"
        elif goal_type == 'hydration':
            if quantity and quantity < 2:
                return "Needs more focus on hydration"
            return "Achievable with increased water intake"

        return "Achievable with a structured approach"
