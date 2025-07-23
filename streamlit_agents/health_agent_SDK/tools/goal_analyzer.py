from agents.run_context import RunContextWrapper
from typing import Any
from agents.tool import FunctionTool
import json

async def analyze_goals(ctx: RunContextWrapper[Any], params_json: str) -> dict:
    try:
        params = json.loads(params_json)
    except json.JSONDecodeError:
        return {"result": "❌ Invalid input format. Please provide valid JSON."}
    
    goal = {
        "target_weight_loss": 5,
        "timeframe": "2 months",
        "recommendations": [
            "Reduce calorie intake by 300",
            "Cardio 3x/week",
            "Strength training 2x/week"
        ]
    }
    ctx.context.goal = goal # Save to context for future reference
    return {"result": goal}

goal_tool = FunctionTool(
    name="GoalAnalyzerTool",
    description="Analyzes user's input and sets a realistic fitness goal.",
    params_json_schema={},
    on_invoke_tool=analyze_goals,
    strict_json_schema=True,
    is_enabled=True,
)