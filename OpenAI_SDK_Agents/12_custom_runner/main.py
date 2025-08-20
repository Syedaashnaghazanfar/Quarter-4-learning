import asyncio
import os

from dotenv import load_dotenv, find_dotenv

from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner, set_tracing_disabled, enable_verbose_stdout_logging
from agents.run import AgentRunner, set_default_agent_runner

_ = load_dotenv(find_dotenv())

# enable_verbose_stdout_logging()

gemini_api_key = os.getenv("GEMINI_API_KEY")

#Reference: https://ai.google.dev/gemini-api/docs/openai
client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)



# #   (1)  Simple Custom Runner  

# class CustomAgentRunner(AgentRunner):  # Here AgentRunner is parent class and we inherited it in CustomAgentRunner to override for custom logic
#     async def run(self, starting_agent, input, **kwargs):
#         print(f"---- CUSTOM RUNNER METHOD ----")
#         return await super().run(starting_agent, input, **kwargs)  # here super is used to call the method of the parent class instead of overriden one



# #   (2)  Runner with modified input you will get user prompt in uppercase during runtime 

# class CustomAgentRunner(AgentRunner):
#     async def run(self, starting_agent, input, **kwargs):
#         print("---- CUSTOM RUNNER METHOD ----")
        
#         modified_input = input.upper()  #Converts into uppercase
#         print(f"Modified input: {modified_input}")
        
#         return await super().run(starting_agent, modified_input, **kwargs)


# # (3)    Custom runner adds disclaimer to every output  

# class CustomAgentRunner(AgentRunner):
#     async def run(self, starting_agent, input, **kwargs):
#         print("---- CUSTOM RUNNER METHOD ----")
#         result = await super().run(starting_agent, input, **kwargs)
        
#         # Example: add disclaimer to every answer
#         result.final_output += "\n\n[Disclaimer: AI-generated, verify before using!]"
        
#         return result


#   (4)     Custom runner with error handling if incorrect model is provided then fallback agent model is used 

class CustomAgentRunner(AgentRunner):
    async def run(self, starting_agent, input, **kwargs):
        try:
            return await super().run(starting_agent, input, **kwargs)
        except Exception as e:
            print(f"\n Primary agent failed: {e}, retrying with fallback model...")
            fallback_agent = Agent(
                name="Fallback Assistant",
                instructions=starting_agent.instructions,
                model=OpenAIChatCompletionsModel(model="gemini-2.0-flash",openai_client=client),
            )
            return await super().run(fallback_agent, input, **kwargs)


# this is model attribute or global attribute [set_default_agent_runner], we pass our new class to it and it sets Runner class to our custom runner we just made i.e CustomAgentRunner
set_default_agent_runner(CustomAgentRunner())

set_tracing_disabled(disabled=True)

async def main():
    # This agent will use the custom LLM provider
    agent = Agent(
        name="Assistant",
        instructions="You only respond in english.",
        model=OpenAIChatCompletionsModel(model="ashna-gpt", openai_client=client),
        
    )

    result = await Runner.run(
        agent,
        "Tell me about recursion in programming. just in one paragraph",
    )
    print("\n",result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
    
