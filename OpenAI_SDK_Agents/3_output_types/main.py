from pydantic import BaseModel
from agents import Agent,Runner
import asyncio

# pydantic is used to import basemodel which is used for defining the output type!

class CalendarEvent(BaseModel):
    name: str
    date: str
    participants: list[str]


async def main():
    
    agent = Agent(
    name="Calendar extractor",
    instructions="Extract calendar events from text",
    output_type=CalendarEvent, #When you pass an output_type, that tells the model to use structured outputs instead of regular plain text responses.
    )

    result = await Runner.run(agent,"What is todays date") #last updated data that is: 10 january,2023 {for getting current date we have to use tools for it}
    print(result.final_output)

asyncio.run(main())