# streaming.py
import asyncio
from typing import AsyncGenerator
from agents import Runner
from openai.types.responses import ResponseTextDeltaEvent

from config import config
from health_agent import health_agent  # ✅ this was missing earlier

async def stream_agent_response(user_input: str, context) -> AsyncGenerator[str, None]:
    result = Runner.run_streamed(
        starting_agent=health_agent,
        input=user_input,
        context=context,
        run_config=config
    )

    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            print("🔄 Streaming token:", event.data.delta)  # Debug line
            yield event.data.delta or ""
        elif event.type == "final_response_event":
            print("✅ Final response received")
            yield event.data.response or ""