from agents import Agent
from guardrails import (
    medical_input_guardrail,
    medical_output_guardrail,
    GenericResponse
)

injury_support_agent = Agent(
    name="Injury Support Agent",
    handoff_description="Specialist agent for injury-related queries",
    instructions="If the user mentions an injury, you will handle the support.You may suggest common at-home care options like rest, ice packs, gentle stretches, or seeing a physiotherapist — but avoid any prescriptions or diagnoses.\nIf the injury is severe or requires medical attention, you will escalate to the Escalation Agent.",
    tools=[],
    hooks=None,
    input_guardrails=[medical_input_guardrail],
    output_guardrails=[medical_output_guardrail],
    output_type=GenericResponse

)