from agents import Agent, Runner, function_tool
from agents import AsyncOpenAI, OpenAIChatCompletionsModel
from dotenv import load_dotenv
import os
import requests

load_dotenv()  # Loads your OPENAI_API_KEY from .env

# --- Step 1: Define the tool ---
@function_tool
def get_weather(city:str)->str:
    """
    Get the current weather for a given city.
    """
    result=requests.get(f"http://api.weatherapi.com/v1/current.json?key=8e3aca2b91dc4342a1162608252604&q={city}")
    data=result.json()
    return f"The current weather in {city} is {data['current']['temp_c']}°C with {data['current']['condition']['text']}."



# --- Step 2: Set up the OpenAI client ---
openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --- Step 3: Define the model using that client ---
model = OpenAIChatCompletionsModel(
    model="gpt-4-turbo",  
    openai_client=openai_client
)

# --- Step 4: Create the agent and add the tool ---
agent = Agent(
    name="WeatherAgent",
    instructions="You are a helpful weather assistant. Use tools to get weather information.",
    tools=[get_weather],
    model=model
)

# --- Step 5: Run the agent with a question ---
result1 = Runner.run_sync(agent, "What is the weather in New York?")
result2 = Runner.run_sync(agent, "What is the weather in London?")
result3 = Runner.run_sync(agent, "What is the weather in Saudia Arabia, Hafar al batin?")
result4 = Runner.run_sync(agent, "What is the weather in Pakistan, Karachi?")
print(result1.final_output)
print(result2.final_output)
print(result3.final_output)
print(result4.final_output)


# you will get the current weather in the specified cities.
# You can add more tools and run the agent with different questions as needed.