from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig
from dotenv import load_dotenv

import os

# Load environment variables from .env file
load_dotenv()
# Get the API key from environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable is not set.")

# Run level means the config and model will be defined at the run level means after we pass Runner.run(here!!)


#Reference: https://ai.google.dev/gemini-api/docs/openai
external_client = AsyncOpenAI(
    api_key= GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

agent: Agent = Agent(name="Assistant", instructions="You are a helpful assistant")

result = Runner.run_sync(agent, "Hello, how are you.", run_config=config)
# if we want to override the config parameter or other parameters for a specific run we would use this overide model RunConfig
# result = Runner.run_sync(agent, "Hello, how are you.", run_config=RunConfig(model=gemini_flash, model_provider=external_client))
# We can also use the run_config to pass in additional parameters like temperature, max_tokens, etc.

print(result.final_output)

# Output :
# Hello! As a large language model, I don't experience feelings like humans do, so I don't have a "how are you" in the same way. But I am functioning optimally and r ready to help you with any questions or tasks you have! How can I assist you today?
# Note: The output may vary based on the model's responses and updates.