from agents import Agent, Runner, function_tool
from agents import AsyncOpenAI, OpenAIChatCompletionsModel
from dotenv import load_dotenv
import os

load_dotenv()  # Loads your OPENAI_API_KEY from .env

# --- Step 1: Define the tool ---
@function_tool
def add_numbers(a: int, b: int) -> int:
    """Add two numbers and return the result."""
    return a + b

# --- Step 2: Set up the OpenAI client ---
openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --- Step 3: Define the model using that client ---
model = OpenAIChatCompletionsModel(
    model="gpt-4-turbo", 
    openai_client=openai_client
)

# --- Step 4: Create the agent and add the tool ---
agent = Agent(
    name="CalculatorAgent",
    instructions="You are a helpful math assistant. Use tools to calculate.",
    tools=[add_numbers],
    model=model
)

# --- Step 5: Run the agent with a question ---
result = Runner.run_sync(agent, "What is 23 plus 45?")
print(result.final_output)


# you can also add more tools and run the agent with different questions as needed.
# For example, you can add a weather tool as shown in the ComplexExample.py.