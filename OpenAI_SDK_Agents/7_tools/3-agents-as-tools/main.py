# Imports
import asyncio
import os
from agents import Agent, Runner, OpenAIChatCompletionsModel
from openai import AsyncOpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up the OpenAI client
openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Define the model using that client 
model = OpenAIChatCompletionsModel(
    model="gpt-4-turbo", 
    openai_client=openai_client
)

# Make multiple agents for different languages
# Each agent will handle translation to a specific language

spanish_agent = Agent(
    name="spanish_agent",
    instructions="You translate the user's message to Spanish",
    model=model
)

french_agent = Agent(
    name="french_agent",
    instructions="You translate the user's message to French",
    model=model
)

italian_agent = Agent(
    name="italian_agent",
    instructions="You translate the user's message to Italian",
    model=model
)

# the orchestrator agent will decide which translation agent to call
# based on the user's request. It will use the tools provided by the other agents.
# It will not translate on its own, but will use the tools to get translations.
# This agent will be the main entry point for the user.

orchestrator_agent = Agent(
    name="orchestrator_agent",
    instructions=(
        "You are a translation agent. You use the tools given to you to translate."
        "If asked for multiple translations, you call the relevant tools in order."
        "You never translate on your own, you always use the provided tools."
    ),
    tools=[
        spanish_agent.as_tool(         #.as_tool() converts the agent to a tool hence you can use agents as tools too!
            tool_name="translate_to_spanish",
            tool_description="Translate the user's message to Spanish",
        ),
        french_agent.as_tool(
            tool_name="translate_to_french",
            tool_description="Translate the user's message to French",
        ),
        italian_agent.as_tool(
            tool_name="translate_to_italian",
            tool_description="Translate the user's message to Italian",
        ),
    ],
    model=model
)


async def main():
    msg = input("Hi! What would you like translated, and to which languages? ")

    orchestrator_result = await Runner.run(orchestrator_agent, msg)
    print(f"\n\nFinal response:\n{orchestrator_result.final_output}")


if __name__ == "__main__":
    asyncio.run(main())


# Output:

# Hi! What would you like translated, and to which languages? hello my name is Ashna to spanish


# Final response:
# The translation of "hello my name is Ashna" to Spanish is: "Hola, mi nombre es Ashna."