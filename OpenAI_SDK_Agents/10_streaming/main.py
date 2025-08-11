import asyncio
from openai.types.responses import ResponseTextDeltaEvent
from agents import Agent, Runner , enable_verbose_stdout_logging,function_tool
from openai.types.responses import ResponseTextDeltaEvent

import os
from dotenv import load_dotenv

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

#for debugging purposes
enable_verbose_stdout_logging()

@function_tool
async def get_weather(city:str) -> str:
    """
    Get the current weather for a given city.
    """
    print(f"Fetching weather for {city}...")
    await asyncio.sleep(5)  # Simulate a delay for the API call
    print("-" * 50)
    return f"The current weather in {city} is sunny with a temperature of 25°C."
  

async def main():
    agent = Agent(
        name="Joker",
        instructions="You are a helpful assistant.",
        tools=[get_weather]
    )

    result = Runner.run_streamed(agent, input="what is biology in 10 words? also give weather for karachi", )
    async for event in result.stream_events():
       
        #  print("\n [EVENT] :", event.type)    #this would print whole event beneath we have filtered it to print only the response text delta event from the RawResponseStreamEvent class
         if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            print("\n [STREAMING RESPONSE] :", event.data.delta)


if __name__ == "__main__":
    asyncio.run(main())

    # task: how to implement error handling like if the response isnt even generating after the sleep mode then the user will not wait for tha pecific time 
    # so how to implement these kind of error handling in this case