from agents import Agent

escalation_agent = Agent(
    name="Escalation Agent",
    handoff_description="Specialist agent for escalated issues",
    instructions="If the users sayd he need to see human or doctor or specialist, you will handle the escalation.",
)