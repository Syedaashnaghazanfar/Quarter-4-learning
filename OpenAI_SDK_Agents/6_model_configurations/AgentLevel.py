import asyncio
from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner
import os 
from dotenv import load_dotenv


#Agent level means the model and config is defined at the agent level means in the agent class

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

#Reference: https://ai.google.dev/gemini-api/docs/openai
client = AsyncOpenAI(
    api_key= GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

async def main():
    # This agent will use the custom LLM provider
    agent = Agent(
        name="Assistant",
        instructions="You only respond in urdu.",
        model=OpenAIChatCompletionsModel(model="gemini-2.5-flash", openai_client=client), #agent level has model being defined here instead of outside
    )

    result = await Runner.run(
        agent,
        "I am learning Agentic AI with Panaversity Community",
    )
    print(result.final_output)  #we cannot define runconfig in the result because it doesnt require the runconfig parameter we define it in agent instead


if __name__ == "__main__":
    asyncio.run(main())

#output:

# یہ بہت اچھی بات ہے۔ ایجنٹک AI ایک دلچسپ اور ابھرتا ہوا شعبہ ہے۔ امید ہے آپ پاناورسٹی کمیونٹی کے ساتھ اچھا سیکھ رہے ہوں گے۔
