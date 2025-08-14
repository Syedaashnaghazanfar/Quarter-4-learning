from dataclasses import dataclass
from agents import Agent, RunContextWrapper,Runner, enable_verbose_stdout_logging, ModelSettings
import asyncio
from agents import function_tool
from agents.agent import StopAtTools

enable_verbose_stdout_logging()

import os
from dotenv import load_dotenv

load_dotenv()
os.getenv("OPENAI_API_KEY")  # Ensure your OpenAI API key is set in the environment

@dataclass
class UserContext:
    id: str
    name: str

@function_tool
def get_user_info(context: RunContextWrapper[UserContext]) -> str:
    """Returns the user's name and ID."""
    return f"Your name is {context.context.name}, and your ID is {context.context.id}."

@function_tool
def get_weather(city: str) -> str:
    """Returns the current weather for a given city."""
    # This is a placeholder implementation. In a real application, you would fetch weather data from an API.
    return f"The current weather in {city} is sunny with a temperature of 25°C."


# function that generates dynamic instructions based on the user's context
def dynamic_instructions(
    context: RunContextWrapper[UserContext], agent: Agent[UserContext]
) -> str:
    return f"The user's name is {context.context.name}. and their id is {context.context.id} Help them with their questions."


agent = Agent[UserContext](
    name="Triage agent",
    instructions=dynamic_instructions,
    tools=[get_user_info, get_weather],  # Register the function tool
    # tool_use_behavior=StopAtTools(stop_at_tool_names="get_weather"),  # Stop at the first tool call , only use the get_weather tool and wont answer other questions
    model_settings=ModelSettings(parallel_tool_calls=False), 
    # reset_tool_choice=True  # Reset tool choice after each run
)

async def main():
    user_context = UserContext(id="12345", name="Ashna")
    result = await Runner.run(agent,"What is the weather in karachi, what is my name and id?",context=user_context)
    print(result.final_output)

asyncio.run(main())

# [User Message]
#     ↓
# LLM Call #1 → Decides: "Call get_weather"
#     ↓
# Tool Execution → returns weather
#     ↓
# LLM Call #2 → Takes original Q + tool results → Produces final answer
#     ↓
# [Assistant Response]
