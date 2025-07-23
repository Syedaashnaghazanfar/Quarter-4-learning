from agents.tool import FunctionTool
from agents.run_context import RunContextWrapper
from typing import Any
import json

# 🏋️ Workout Recommendation Tool (Dynamic and Context-Aware)
async def recommend_workout(ctx: RunContextWrapper[Any], params_json: str):
    try:
        params = json.loads(params_json)
        goal = params.get("goal", "general fitness").lower()
        fitness_level = params.get("fitness_level", "beginner").lower()
    except Exception:
        return {"result": "❌ Invalid input format. Please provide 'goal' and 'fitness_level'."}

    # 🧠 Logic to personalize based on user input
    if goal == "weight loss":
        if fitness_level == "beginner":
            workout_plan = {
                "type": "Cardio + Bodyweight",
                "duration": "30 minutes",
                "frequency": "4 times/week"
            }
        else:
            workout_plan = {
                "type": "HIIT + Light Weights",
                "duration": "45 minutes",
                "frequency": "5 times/week"
            }

    elif goal == "muscle gain":
        workout_plan = {
            "type": "Strength Training + Progressive Overload",
            "duration": "60 minutes",
            "frequency": "4-5 times/week"
        }

    elif goal == "flexibility":
        workout_plan = {
            "type": "Yoga + Stretching",
            "duration": "40 minutes",
            "frequency": "3-4 times/week"
        }

    else:
        workout_plan = {
            "type": "Full Body Routine",
            "duration": "30-45 minutes",
            "frequency": "3 times/week"
        }

    # 🔒 Save in context if needed for future reference
    ctx.context.workout_plan = workout_plan
    return {"result": workout_plan}

# ✅ Register Tool with JSON Schema
workout_tool = FunctionTool(
    name="WorkoutRecommenderTool",
    description="Recommends a personalized workout plan based on user's goal and fitness level.",
    params_json_schema={
        "type": "object",
        "properties": {
            "goal": {
                "type": "string",
                "description": "User's fitness goal, e.g., weight loss, muscle gain, flexibility"
            },
            "fitness_level": {
                "type": "string",
                "enum": ["beginner", "intermediate", "advanced"],
                "description": "User's current fitness level"
            }
        },
        "required": ["goal", "fitness_level"]
    },
    on_invoke_tool=recommend_workout,
    strict_json_schema=True,
    is_enabled=True,
)