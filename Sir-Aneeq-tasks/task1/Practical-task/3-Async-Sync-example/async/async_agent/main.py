import os
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig
import asyncio  # Asynchronous ka magic module

# .env file se environment variables load karo
load_dotenv()

# Gemini ka API key uthao
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY not set in environment variables!")

# Gemini API ke liye external client
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# Model banado
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

# Configuration tayyar
config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

# Asynchronous main function banado
async def main():
    # Agent banado
    agent = Agent(
        name="Assistant",
        instructions="You are a helpful assistant.",
        model=model
    )

    # Yeh asynchronous hai - rukne ki zarurat nahi, dusre kaam bhi chalte rahenge
    result = await Runner.run(agent, "Tell me about recursion in programming.", run_config=config)

    print("\nCALLING AGENT\n")
    print(result.final_output)

# Python ka event loop chalao
if __name__ == "__main__":
    asyncio.run(main())
