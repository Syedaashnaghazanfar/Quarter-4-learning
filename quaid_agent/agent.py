from agents import Agent, OpenAIChatCompletionsModel, Runner, set_tracing_disabled #type: ignore
import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
import asyncio

#loading environment variables from .env file
load_dotenv()

# Get the Gemini API key from environment variables
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Check if the API key is set
#the AsyncOpenAI client is used to interact with the Gemini API

client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)
# Disable tracing to avoid unnecessary logging

set_tracing_disabled(disabled=True)

#The OpenAIChatCompletionsModel is used to create a model instance for the agent
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=client
)

# The main function initializes the agent and runs it with a specific query
#async function is used because the agent and model interactions are asynchronous
async def main():
    agent = Agent(
        name="Quaid Agent",
        description="An agent that can provide information about Quaid e Azam.",
        instructions="You are a helping assistant. Your name is Agent Quaid.",
        model=model
    )
# The agent is run with a specific query to get information about Quaid e Azam
    result = await Runner.run(
        agent,
        "Who was Quaid e Azam? Give documentry about him",
        
    )

    print(result.final_output)

#here asyncio.run is used to run the main function as we have async functions used here
if __name__ == "__main__":
    asyncio.run(main())    
