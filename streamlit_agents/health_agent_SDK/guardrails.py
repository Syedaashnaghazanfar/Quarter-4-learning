# guardrails.py

from pydantic import BaseModel
from typing import Any, Union
from agents import (
    Agent,
    GuardrailFunctionOutput,
    RunContextWrapper,
    Runner,
    TResponseInputItem,
    input_guardrail,
    output_guardrail
)
from config import model


# ===========================
# 🛡️ Input Guard
# ===========================

class MedicalViolationOutput(BaseModel):
    violates_policy: bool
    reason: str

input_guardrail_agent = Agent(
    name="InputModerationAgent",
    instructions="""
    Check if the user is asking for:
    - a medical diagnosis
    - emergency treatment
    - prescriptions or therapy plans
    """,
    output_type=MedicalViolationOutput,
    model=model
)

@input_guardrail
async def medical_input_guardrail(
    ctx: RunContextWrapper[None],
    agent: Agent,
    input: Union[str, list[TResponseInputItem]]
) -> GuardrailFunctionOutput:
    result = await Runner.run(input_guardrail_agent, input, context=ctx.context)
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.violates_policy
    )


# ===========================
# 🛡️ Output Guard
# ===========================

class UnsafeOutputCheck(BaseModel):
    is_risky: bool
    reasoning: str

class GenericResponse(BaseModel):
    response: str  # Any text response from the agent

output_guardrail_agent = Agent(
    name="OutputModerationAgent",
    instructions="""
    Check if the output includes:
    - diagnosis
    - medication advice
    - therapy plans
    - emergency treatment suggestions
    """,
    output_type=UnsafeOutputCheck,
    model=model
)

@output_guardrail
async def medical_output_guardrail(
    ctx: RunContextWrapper,
    agent: Agent,
    output: GenericResponse  # Works with any agent's text output
) -> GuardrailFunctionOutput:
    result = await Runner.run(output_guardrail_agent, output.response, context=ctx.context)
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.is_risky
    )