from agents.tool import FunctionTool  

# 📈 Progress Tracker Tool

def track_progress(input, context):
    
    if not hasattr(context.context, "progress_logs"):
        context.context.progress_logs = []

    context.context.progress_logs.append({"update": input})
    return {"result": "Progress logged"}

# ✅ Define tool using FunctionTool
tracker_tool = FunctionTool(
    name="ProgressTrackerTool",
    description="Logs the user's progress updates.",
    params_json_schema={
        "type": "object",
        "properties": {
            "input": {
                "type": "string",
                "description": "Progress update from the user"
            }
        },
        "required": ["input"]
    },
    on_invoke_tool=track_progress,
    strict_json_schema=True,
    is_enabled=True,
)