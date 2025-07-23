from agents import AgentHooks
from agents.run_context import RunContextWrapper
from agents.tool import ToolCall
from agents.agent import Agent
from agents.tool import FunctionTool
import logging
from typing import Any

# Setup logging
logging.basicConfig(level=logging.INFO)

class CustomHooks(AgentHooks):

    async def on_tool_start(
        self,
        run_context: RunContextWrapper[Any],
        agent: Agent[Any],
        tool_call: ToolCall,
        tool: FunctionTool
    ):
        user = getattr(run_context.context, "name", "Unknown User")
        logging.info(f"🛠️ Tool '{tool.name}' started for {user}")

    async def on_handoff(
        self,
        run_context: RunContextWrapper[Any],
        agent: Agent[Any]
    ):
        user = getattr(run_context.context, "name", "Unknown User")
        logging.info(f"🤝 Handoff to agent '{agent.name}' for {user}")