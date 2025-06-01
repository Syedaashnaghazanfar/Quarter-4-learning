import os
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig

# .env file se environment variables load karo
load_dotenv()

# Gemini ka API key uthao
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY not set in environment variables!")

# Gemini API ke liye external client
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# Model banado
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

# Configuration tayyar
config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

# Agent banado jo help karega
agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant.",
    model=model
)

# Yeh synchronous hai - ruk jao jab tak result aaye
result = Runner.run_sync(agent, "Hello, how are you.", run_config=config)

print("\nCALLING AGENT\n")
print(result.final_output)
