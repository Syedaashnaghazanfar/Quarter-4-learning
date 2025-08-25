import os
from dotenv import find_dotenv, load_dotenv
from openai import AsyncOpenAI
from pydantic import BaseModel
from agents import Agent, handoff, RunContextWrapper, Runner, set_tracing_disabled, OpenAIChatCompletionsModel, function_tool
import asyncio
from agents.extensions import handoff_filters
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX


_ = load_dotenv(find_dotenv())

gemini_api_key = os.getenv("GEMINI_API_KEY")

client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

set_tracing_disabled(disabled=True)

class EscalationData(BaseModel):
    reason: str

class Location(BaseModel):
    lat: float
    long: float

@function_tool
async def fetch_weather(location: Location) -> str:
    """Fetch the weather for a given location."""
    return f"the weather of lat:{location.lat}, long:{location.long} is sunny"

def on_handoff(ctx: RunContextWrapper[None], input_data: EscalationData):
    print(f"🔄 HANDOFF TRIGGERED! Reason: {input_data.reason}")
    return {"message": "Successfully handed off to Secondary Agent!"}

# Secondary agent for recursion questions
secondary_agent = Agent(
    name="Recursion Expert",
    instructions="You are an expert in programming. Explain recursion concepts clearly and simply.",
    handoff_description="Handles programming concepts like recursion.",
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
)

# Handoff tool
handoff_tool = handoff(
    agent=secondary_agent,
    on_handoff=on_handoff,
    tool_name_override="escalate_to_recursion_expert",
    tool_description_override="Use this tool when the user asks about recursion, recursive functions, or programming concepts that require expert explanation.",
    input_type=EscalationData,
    input_filter=handoff_filters.remove_all_tools,
)

# Main agent with explicit instructions to use handoff
main_agent = Agent(
    name="Main Assistant",
    
# Using RECOMMENDED_PROMPT_PREFIX so the assistant understands it's in a team and will always trigger handoff if present 
# This helps it know when to call in another agent instead of trying to do everything itself.

    instructions=f"""{RECOMMENDED_PROMPT_PREFIX} You are a helpful assistant. You can answer general questions and fetch weather information.
    
    IMPORTANT: If the user asks about recursion, recursive functions, or programming concepts that you're not confident about, you MUST use the 'escalate_to_recursion_expert' tool to get expert help.""",
    handoffs=[handoff_tool],
    tools=[fetch_weather],
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
)

async def test_handoff():
    # Test 1: Weather query (should NOT trigger handoff)
    print("=== Test 1: Weather Query ===")
    result1 = await Runner.run(main_agent, "What's the weather in Karachi? Latitude 24.86, longitude 67.01")
    print(f"Weather result: {result1.final_output}\n")
    
    # Test 2: Recursion query (SHOULD trigger handoff)
    print("=== Test 2: Recursion Query ===")
    result2 = await Runner.run(main_agent, "What is recursion in programming?")
    print(f"Recursion result: {result2.final_output}\n")
    
    # Test 3: Mixed query (should handle both but if used remove_all_tools in input filter the weather tool will not work!)
    print("=== Test 3: Mixed Query ===")
    result3 = await Runner.run(main_agent, "What's recursion and also the weather in Karachi? Use lat 24.86, long 67.01")
    print(f"Mixed result: {result3.final_output}")

if __name__ == "__main__":
    asyncio.run(test_handoff())
