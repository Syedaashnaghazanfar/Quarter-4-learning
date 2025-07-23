from agents.tool import FunctionTool
from agents.run_context import RunContextWrapper
from typing import Any
import json

async def meal_planner(ctx: RunContextWrapper[Any], params_json: str) -> dict:
    try:
        data = json.loads(params_json)
        user_goal = data.get("goal", "").lower().strip()
    except Exception:
        user_goal = ""

    # 🥗 Meal planning logic based on user goal
    if "weight" in user_goal:
        plan = (
            "🥗 Meal plan to help with weight loss:\n"
            "- 🥣 Breakfast: Greek yogurt with chia seeds and berries\n"
            "- 🥗 Lunch: Quinoa salad with chickpeas and veggies\n"
            "- 🍲 Dinner: Grilled chicken with steamed broccoli\n"
            "- 💧 Hydration: Drink at least 8 glasses of water"
        )
    elif "muscle" in user_goal or "gain" in user_goal:
        plan = (
            "💪 Muscle-building meal plan:\n"
            "- 🍳 Breakfast: 3 eggs, whole grain toast, avocado\n"
            "- 🥩 Lunch: Grilled beef/chicken with brown rice and spinach\n"
            "- 🧆 Dinner: Lentils with sweet potato and mixed veggies\n"
            "- 🥤 Post-workout: Protein smoothie with banana and peanut butter"
        )
    elif "Vegetarian" in user_goal:
        plan = (
            "🌱 Vegetarian-friendly plan:\n"
            "- 🍌 Breakfast: Oatmeal with almond milk, banana, and flaxseeds\n"
            "- 🥙 Lunch: Hummus wrap with grilled veggies\n"
            "- 🍛 Dinner: Tofu stir-fry with brown rice and cashews"
        )
    else:
        plan = (
            "🍽️ General healthy meal plan:\n"
            "- 🍳 Breakfast: Oatmeal with fruits and nuts\n"
            "- 🥗 Lunch: Grilled chicken or chickpea salad\n"
            "- 🍚 Dinner: Steamed vegetables with quinoa or brown rice\n"
            "- 🍎 Snacks: Fresh fruits, yogurt, or almonds\n"
            "- 💧 Stay hydrated throughout the day"
        )

    # Save to context (if needed)
    ctx.context.meal_plan = plan

    return {"result": plan}


meal_tool = FunctionTool(
    name="MealPlannerTool",
    description="Generates a healthy meal plan based on user dietary goals like weight loss, muscle gain, or vegan preference.",
    params_json_schema={
        "type": "object",
        "properties": {
            "goal": {
                "type": "string",
                "description": "The user's dietary goal (e.g., 'weight loss', 'muscle gain', 'Vegetarian')"
            }
        },
        "required": []
    },
    on_invoke_tool=meal_planner,
    strict_json_schema=True,
    is_enabled=True,
)