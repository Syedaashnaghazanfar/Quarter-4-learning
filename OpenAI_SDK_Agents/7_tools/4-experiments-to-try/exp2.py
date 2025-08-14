from dataclasses import dataclass
from agents import Agent, RunContextWrapper, Runner, enable_verbose_stdout_logging, ModelSettings
import asyncio
from agents import function_tool

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
    return f"The current weather in {city} is sunny with a temperature of 25°C."

@function_tool
def add_num(num1: int, num2: int) -> int:
    """Returns the sum of two numbers."""
    return num1 + num2

def dynamic_instructions(
    context: RunContextWrapper[UserContext], agent: Agent[UserContext]
) -> str:
    return f"The user's name is {context.context.name}, and their id is {context.context.id}. Help them with their questions."

agent = Agent[UserContext](
    name="Triage agent",
    instructions=dynamic_instructions,
    tools=[get_user_info, get_weather, add_num],
    model_settings=ModelSettings(parallel_tool_calls=False)  # Force sequential tool calls, when we were not using this the llm was taking two turns no matter how many tools we use but after doing it false the tools wont run parallel and llm will take turns according to the number of tools present 

)

async def main():
    user_context = UserContext(id="12345", name="Ashna")
    result = await Runner.run(
        agent,
        "What is the weather in karachi, add 4 and 4, what is my name and id?",
        context=user_context
    )
    print(result.final_output)

asyncio.run(main())


# [User Message]
#   ↓
# LLM Call #1  →  Decides: "Call get_weather" (extracts city='karachi')
#   ↓
# Tool Execution #1  →  get_weather("karachi") → returns "Sunny, 25°C"
#   ↓
# LLM Call #2  →  Takes original Q + weather → Decides: "Call add_num" (4, 4)
#   ↓
# Tool Execution #2  →  add_num(4, 4) → returns 8
#   ↓
# LLM Call #3  →  Takes original Q + weather + sum → Produces final full answer
#   ↓
# [Assistant Response]
#   - Weather in Karachi: Sunny, 25°C
#   - Sum of 4 and 4: 8
#   - Name & ID from context: Ashna, 12345


# the output depends on llms intellegence 
# if we will don max_turns=2 it will throw error bcoz it will not be able to calls tools and final llm response