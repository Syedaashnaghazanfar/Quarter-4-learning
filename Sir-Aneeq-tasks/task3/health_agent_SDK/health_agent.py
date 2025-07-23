from agents import Agent
from tools.meal_planner import meal_tool
from tools.tracker import tracker_tool
from tools.scheduler import scheduler_tool
from tools.workout_recommender import workout_tool
# from tools.memory_tool import memory_tool_fn
from tools.goal_analyzer import goal_tool
from handoff_agents.nutrition_expert_agent import nutrition_expert_agent
from handoff_agents.injury_support_agent import injury_support_agent
from handoff_agents.escalation_agent import escalation_agent
from config import model

# Optional: Load hooks for memory/tool tracking
try:
    from hooks import CustomHooks
    hooks = CustomHooks()
except ImportError:
    hooks = None

# ✅ Create the Health Agent
health_agent = Agent(
    name="HealthAgent",
    instructions=(
        "You are HealthAgent, a compassionate and intelligent assistant for health and wellness.\n\n"

"🧠 You keep track of what the user says using memory.\n"
"Every time the user sends a message, save it in memory before responding.\n\n"

"🛠️ You have access to tools for generating meal plans, workouts, schedules, and health tracking.\n"
"Use only one tool at a time to complete each task.\n"
"Never combine or merge tool names. Use each tool separately as needed.\n\n"

"📜 When the user asks to review previous inputs, refer to stored history from memory.\n"

"🤝 If a user’s request involves complex health or nutrition needs, delegate to the appropriate expert agent.\n"

"✨ Always respond with helpful, friendly, and encouraging messages.\n"
    ),
    tools=[
        goal_tool,
        # memory_tool_fn,
        meal_tool,
        tracker_tool,
        scheduler_tool,
        workout_tool
    ],
    handoffs=[
        escalation_agent,
        nutrition_expert_agent,
        injury_support_agent
    ],
    model=model,
    hooks=hooks
)

# ✅ Tool name validation
for tool in health_agent.tools:
    if not hasattr(tool, 'name') or not tool.name:
        raise ValueError(f"Tool {tool} is missing a 'name' attribute")
    if not tool.name.isidentifier():
        raise ValueError(f"Invalid tool name '{tool.name}'")

print("✅ HealthAgent configured successfully")