import asyncio
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled
import os
from dotenv import load_dotenv

# Context Using Agent Context

# Load environment variables from .env file
load_dotenv()

set_tracing_disabled(True)

# Get Gemini API key from environment
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set.")

# Setup Gemini client and model
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

async def main():
    user_name = "Ashna Ghazanfar"
    current_date = "2025-08-09"

    # Agent/LLM context embedded directly in instructions (system prompt)
    agent = Agent(
        name="GeminiAgent",
        model=model,
        instructions=f"""
        You are a friendly assistant helping {user_name}.
        Today's date is {current_date}.
        Always greet them by name and answer in a warm, conversational tone.
        """
    )

    # Run the agent - no local context, just input
    result = await Runner.run(
        starting_agent=agent,
        input="What should I do today?"
    )

    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())


# Agent or LLM context is embedded directly in the instructions. it is not stored in a separate context variable and is visible to the agent.
# Local context is the context for private information that the agent can use to answer questions. but still agent cannot see the context.
# The agent is designed to be friendly and conversational, greeting the user by name and providing warm responses.

# Output:

# Hi Ashna, how are you today? Since it's August 9, 2025, here are a few ideas for things you could do:

# *   **Relax and Recharge:** Take some time for self-care. You could read a book, take a bath, meditate, or listen to your favorite music.

# *   **Get Active:** Go for a walk, run, or bike ride. Exercise can be a great way to boost your mood and energy levels.

# *   **Connect with Loved Ones:** Spend time with family or friends. Have a conversation, play a game, or share a meal.

# *   **Explore Your Interests:** Work on a hobby, visit a museum, or try something new. This is a great opportunity to learn something new or pursue your passions.

# *   **Plan Something Fun:** Look ahead and plan a future activity to look forward to.

# Is there anything specific you had in mind or anything I can help you with further?