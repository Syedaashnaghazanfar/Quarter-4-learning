from agents import Agent, handoff, RunContextWrapper, Runner
import asyncio

# This function will be triggered when the handoff is executed
def on_handoff(ctx: RunContextWrapper[None]):
    print("⚡ Handoff called! Transferring to Secondary Agent...")
    return {"message": "Switched to Secondary Agent via handoff!"}

# Define the agent that handles recursion questions
secondary_agent = Agent(
    name="Secondary Agent",
    instructions="You are an expert in programming. When the user asks about recursion, explain it clearly and simply.",
    handoff_description="Handles programming concepts like recursion."
)
 
# This handoff function used here is basically used for overidding the name and description we can also just create simple secondary_agent and pass the handoff of the secondary_agent
# Define the handoff — this tells the SDK when and where to switch agents
handoff_tool = handoff(
    agent=secondary_agent,
    on_handoff=on_handoff,
    tool_name_override="custom_handoff_tool",
    tool_description_override="If a question is about recursion, forward it to Secondary Agent.",
)


# Define your main agent that includes the handoff logic
main_agent = Agent(
    name="Main Agent",
    handoffs=[handoff_tool],  # 🔁 Not tools — goes into handoffs
)

# Run the full interaction
async def agent():
    user_question = "What is recursion in programming?"  #when user asks about who is Elon Musk  the handoff will not be triggered
    print(f"👩‍💻 User asked: {user_question}")
    result = await Runner.run(main_agent, user_question)
    print("✅ Final Result:", result)

asyncio.run(agent())
