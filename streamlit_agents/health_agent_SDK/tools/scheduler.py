import json
from typing import Any
from agents.tool import FunctionTool


async def schedule_checkin_tool(context: Any, params_json: str):
    try:
        params = json.loads(params_json)
    except json.JSONDecodeError:
        return {"result": "❌ Invalid input format. Please provide valid JSON."}
    if not hasattr(context.context, "progress_logs") or context.context.progress_logs is None:
        context.context.progress_logs = []

    context.context.progress_logs.append({
        "date": "Weekly",  # or use actual datetime
        "note": "Scheduled weekly check-in"
    })

    return {"result": "✅ Weekly check-in has been successfully scheduled!"}

# ✅ Register with FunctionTool
scheduler_tool = FunctionTool(
    name="CheckinSchedulerTool",
    description="Schedules a weekly check-in for the user.",
    params_json_schema={
        "type": "object",
        "properties": {},
        "required": []
    },
    on_invoke_tool=schedule_checkin_tool,
    strict_json_schema=True,
    is_enabled=True,
)