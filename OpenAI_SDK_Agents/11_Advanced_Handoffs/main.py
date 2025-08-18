from agents import Agent, OpenAIChatCompletionsModel, RunContextWrapper, handoff,Runner,enable_verbose_stdout_logging,function_tool, set_tracing_disabled
import os
from dotenv import load_dotenv
import asyncio
from agents.extensions import handoff_filters
from openai import AsyncOpenAI
from pydantic import BaseModel

class CurrentUser(BaseModel):
   is_logged_in:bool
   bill: str = "200 rs"  


enable_verbose_stdout_logging()

#loading environment variables from .env file
load_dotenv()

# Get the Gemini API key from environment variables
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Check if the API key is set
#the AsyncOpenAI client is used to interact with the Gemini API

client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)
# Disable tracing to avoid unnecessary logging

set_tracing_disabled(disabled=True)

#The OpenAIChatCompletionsModel is used to create a model instance for the agent
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=client
)



@function_tool
def get_weather(city:str)->str:
   return f"The weather in {city} is sunny"

async def can_custumer_refund(context: RunContextWrapper[CurrentUser] ,agent:Agent[CurrentUser])->bool:
   print("\nlocal context:",context)
   if context.context and context.context.is_logged_in:
       return True
   return  False

async def can_custumer_bill(context: RunContextWrapper[CurrentUser] ,agent:Agent[CurrentUser])->bool:
   print("\nlocal context:",context)
   if context.context and context.context.is_logged_in:
       return True
   return  False

billing_agent = Agent[CurrentUser](
   name="Billing agent",
   model=model,
   instructions="You are a billing agent. The user's bill is: {context.bill}. Provide information about their bill."  #still it will not be accessed coz the agent cannot read this is local context and it can only be properly read in tools
)
refund_agent = Agent(name="Refund agent",model=model)


# the handoff function is basically used to override the names and description along with additional details
triage_agent = Agent(
   name="Triage agent", 
   model= model,
   handoffs=[
      handoff(
         agent=refund_agent, 
         tool_name_override="refund_order", # for overriding tool name
         tool_description_override="this is a refund order agent to ahndle refunds requets", #for overriding tool description when u enable verbos you can see the change names and description
         is_enabled=can_custumer_refund,
         # input_filter=handoff_filters.remove_all_tools  #this is going to remove ALL tools while running!note that while using this the tools will not be able to deliver the answer
      ),
      handoff(
         agent=billing_agent,
         is_enabled=can_custumer_bill
      )
   ],

   tools=[get_weather]
   )

async def main():
   # Create current_user with bill context
   current_user = CurrentUser(is_logged_in=True, bill="200 rs")
   
   # Example of accessing bill context in billing agent
   billing_result = await Runner.run(
      billing_agent,
      "What is my current bill amount?",
      context=current_user
   )
   print("\nBilling Agent Output:", billing_result.final_output)
   
   # Original triage agent run
   result = await Runner.run(
      triage_agent,
      "I want to refund my order, [details]:order id :123,amount:100, reason: i want to refund it, also give weather for karachi, What is my bill??",
      context=current_user
   )
   print("\n FINAL OUTPUT:",result.final_output)
   print("\n LAST AGENT:",result.last_agent.name)
  


if __name__ == "__main__":
   asyncio.run(main())

# NOTES:
# * Only one handoff occurs at a time - the triage agent will transfer to exactly one other agent per interaction
# * The handoff function is used to override and customize handoff behavior, including tool names, descriptions, and enablement conditions
# * Input filters are used to control what data gets passed to the target agent during handoff. The built-in parameter `remove_all_tools` removes all tools from the context at runtime
