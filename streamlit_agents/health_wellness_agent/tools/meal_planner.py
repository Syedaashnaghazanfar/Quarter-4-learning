"""
Meal Planner Tool - Builds a personalized 7-day meal plan based on dietary preferences and goals.
"""

from typing import Dict, Any, List
from context import RunContextWrapper
from guardrails import GuardrailValidator
from hooks import hook_manager

class MealPlannerTool:
    """
    Handles generation of structured weekly meal plans tailored to dietary preference and health goals.
    """

    def __init__(self):
        self.name = "meal_planner"

    def build_weekly_plan(self, user_diet_input: str, user_goal: Dict[str, Any], context_wrapper: RunContextWrapper) -> Dict[str, Any]:
        """
        Entry point for generating the 7-day meal plan.
        Validates dietary preference, generates meal schedule, and logs it in the session.
        """
        hook_manager.log_tool_start(self.name)

        try:
            # Step 1: Validate dietary preference
            validated_diet = GuardrailValidator.validate_dietary_input(user_diet_input)

            # Step 2: Generate daily plan
            structured_plan = self._generate_structured_plan(validated_diet, user_goal)

            # Step 3: Save into user context
            context_wrapper.update_context(
                diet_preferences=validated_diet,
                meal_plan=structured_plan["daily_plans"]
            )
            context_wrapper.get_context().add_progress_log("meal_planning", f"Meal plan created for {validated_diet}")

            # Step 4: Final response payload
            response = {
                "response_type": "meal_plan",
                "content": structured_plan
            }

            return GuardrailValidator.validate_output(response)

        except Exception as e:
            return {
                "response_type": "error",
                "content": {"error": str(e)}
            }

    def _generate_structured_plan(self, diet_type: str, goal: Dict[str, Any]) -> Dict[str, Any]:
        """
        Builds the core weekly plan with randomized meal suggestions per day.
        """
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

        meal_templates = self._get_template_library()

        selected_template = meal_templates.get(diet_type, meal_templates["omnivore"])

        weekly_schedule = []
        for i, day in enumerate(days):
            daily_entry = {
                "day": day,
                "meals": {
                    "breakfast": selected_template["breakfast"][i % len(selected_template["breakfast"])],
                    "lunch": selected_template["lunch"][i % len(selected_template["lunch"])],
                    "dinner": selected_template["dinner"][i % len(selected_template["dinner"])],
                    "snack": selected_template["snack"][i % len(selected_template["snack"])]
                },
                "calories": self._estimate_calories(goal)
            }
            weekly_schedule.append(daily_entry)

        return {
            "dietary_type": diet_type,
            "daily_plans": weekly_schedule,
            "tips": self._get_nutrition_tips(diet_type)
        }

    def _estimate_calories(self, goal: Dict[str, Any]) -> int:
        """
        Simple calorie estimate based on goal type.
        """
        base = 2000
        if goal.get("goal_type") == "weight_loss":
            return base - 300
        if goal.get("goal_type") == "weight_gain":
            return base + 300
        return base

    def _get_nutrition_tips(self, diet_type: str) -> List[str]:
        """
        Provides dietary tips based on eating pattern.
        """
        tips_catalog = {
            "vegetarian": ["Include protein at each meal", "Consider B12 supplementation"],
            "vegan": ["Combine complementary proteins", "Take B12 and D3 regularly"],
            "keto": ["Stay hydrated", "Keep an eye on electrolyte intake"],
            "omnivore": ["Eat a variety of whole foods", "Include fiber and greens daily"]
        }

        return tips_catalog.get(diet_type, ["Eat whole, balanced meals", "Drink water throughout the day"])

    def _get_template_library(self) -> Dict[str, Dict[str, List[str]]]:
        """
        Returns all available meal templates categorized by diet type.
        """
        return {
            "vegetarian": {
                "breakfast": ["Oatmeal with berries", "Veggie scramble", "Smoothie bowl", "Avocado toast"],
                "lunch": ["Quinoa salad", "Vegetable soup", "Caprese sandwich", "Buddha bowl"],
                "dinner": ["Pasta primavera", "Stuffed peppers", "Vegetable stir-fry", "Lentil curry"],
                "snack": ["Greek yogurt", "Mixed nuts", "Fruit", "Hummus with veggies"]
            },
            "vegan": {
                "breakfast": ["Chia pudding", "Smoothie bowl", "Oatmeal", "Avocado toast"],
                "lunch": ["Quinoa bowl", "Veggie wrap", "Salad", "Soup"],
                "dinner": ["Tofu stir-fry", "Lentil curry", "Vegetable pasta", "Buddha bowl"],
                "snack": ["Nuts", "Fruit", "Vegetables", "Plant yogurt"]
            },
            "keto": {
                "breakfast": ["Eggs and bacon", "Avocado", "Keto smoothie", "Cheese omelet"],
                "lunch": ["Chicken salad", "Zucchini noodles", "Keto bowl", "Lettuce wraps"],
                "dinner": ["Salmon", "Steak", "Chicken thighs", "Pork chops"],
                "snack": ["Cheese", "Nuts", "Olives", "Fat bombs"]
            },
            "omnivore": {
                "breakfast": ["Eggs", "Oatmeal", "Smoothie", "Toast"],
                "lunch": ["Chicken salad", "Sandwich", "Soup", "Bowl"],
                "dinner": ["Grilled chicken", "Fish", "Pasta", "Stir-fry"],
                "snack": ["Yogurt", "Fruit", "Nuts", "Vegetables"]
            },
            "default": {
                "breakfast": ["Eggs", "Oatmeal", "Smoothie", "Toast"],
                "lunch": ["Chicken salad", "Sandwich", "Soup", "Bowl"],
                "dinner": ["Grilled chicken", "Fish", "Pasta", "Stir-fry"],
                "snack": ["Yogurt", "Fruit", "Nuts", "Vegetables"]
            },

        }
