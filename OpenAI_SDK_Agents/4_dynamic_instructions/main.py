from dataclasses import dataclass
from agents import Agent, RunContextWrapper,Runner
import asyncio


# Example of a dynamic instruction agent that uses the user's context to provide personalized instructions. 
#context is a dataclass that holds the user's information. it also saves our information like we can use it further if we want
@dataclass
class UserContext:
    id: str
    name: str

# function that generates dynamic instructions based on the user's context
def dynamic_instructions(
    context: RunContextWrapper[UserContext], agent: Agent[UserContext]
) -> str:
    return f"The user's name is {context.context.name}. and their id is {context.context.id} Help them with their questions."

# Create an agent that uses the dynamic instructions function to generate its instructions
agent = Agent[UserContext](
    name="Triage agent",
    instructions=dynamic_instructions,
)

async def main():
    user_context = UserContext(id="12345", name="Alice")
    result = await Runner.run(agent,"what is my name and id? also tell me about life!",context=user_context)
    print(result.final_output)

asyncio.run(main())


#output
#Your name is Alice, and your ID is 12345. As for life, it's a fascinating journey filled with experiences, challenges, and growth. It's about finding purpose, forging connections, and exploring the world around us. Embracing change and learning from each moment can make the journey meaningful and rewarding. How are you finding your journey
# This is just a simple example using dynamic instructions we will further learn to  implement these in various ways
