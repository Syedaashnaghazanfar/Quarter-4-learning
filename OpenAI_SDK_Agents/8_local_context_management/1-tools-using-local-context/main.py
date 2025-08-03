import asyncio
from dataclasses import dataclass
from agents import Agent, RunContextWrapper, Runner, function_tool , OpenAIChatCompletionsModel
import os
from dotenv import load_dotenv
from openai import AsyncOpenAI



# Load environment variables from .env file
load_dotenv()

# Set up the OpenAI client
openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Define the model using that client 
model = OpenAIChatCompletionsModel(
    model="gpt-4-turbo", 
    openai_client=openai_client
)

# dataclass is used to define the structure of the user information or saving the data in context
@dataclass
class UserInfo1:
    name: str
    uid: int
    location: str = "Pakistan"


# Define function tools that will be used by the agent to fetch user information along with using context using RunContextWrapper
# RunContextWrapper is used to wrap the context and pass it to the function tool
# function_tool decorator is used to define the function as a tool that can be used by the agent
# The function tool can access the context using the RunContextWrapper


@function_tool
async def fetch_user_age(wrapper: RunContextWrapper[UserInfo1]) -> str:
    '''Returns the age of the user.'''
    return f"User {wrapper.context.name} is 18 years old"

@function_tool
async def fetch_user_location(wrapper: RunContextWrapper[UserInfo1]) -> str:
    '''Returns the location of the user.'''
    return f"User {wrapper.context.name} is from {wrapper.context.location}"

# Main function to run the agent and fetch user information
async def main():
    user_info = UserInfo1(name="Ashna Ghazanfar", uid=123)

    agent = Agent[UserInfo1](
        name="Assistant",
        tools=[fetch_user_age,fetch_user_location],
        model=model
    )

    result = await Runner.run(
        starting_agent=agent,
        input="What is the name of the user? What is the age of the user? current location of his/her?",
        context=user_info,
    )

    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())

# This code defines an agent that can fetch user information using function tools and context.

# Output:
# The agent will respond with the user's name, age, and location based on the provided context
# and the function tools defined.

# Example output:
# The user's name is Ashna Ghazanfar. Ashna is 18 years old and is from Pakistan.