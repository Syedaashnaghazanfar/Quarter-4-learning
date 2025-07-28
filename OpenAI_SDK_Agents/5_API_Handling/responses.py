# OpenAI’s Responses API (stateful, tool‑ready)

# This example uses the OpenAI Python client library to interact with the Responses API.
# It has build in tools and stateful memory, so you can ask follow-up questions without resending the entire conversation history.

from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()

# 1️⃣ Ask with a tool & store memory
r1 = client.responses.create(
    model="gpt-4o-mini",
    input="Search the latest AI news in healthcare.",
    store=True,
    tools=[{"type":"web_search_preview"}]
)

# 2️⃣ Follow‑up (no need to resend history)
r2 = client.responses.create(
    model="gpt-4o-mini",
    previous_response_id=r1.id,
    input="Summarize those findings in bullet points."
)

print(r2.output[0].content[0].text)


# We asked about the latest AI news in healthcare, and then summarized the findings. and the in other response without providing it the entire conversation history, we asked to summarize the findings.
# The Responses API automatically handles state and tools, making it easy to build interactive applications.


# Output:
# Here are the summarized findings in bullet points:

# - **AI Reduces Medical Errors**:
#   - AI tool "AI Consult" reduced diagnostic errors by 16% and treatment errors by 13% in Kenyan clinics, enhancing clinician confidence.

# - **Autonomous Surgery**:
#   - A surgical robot successfully performed gallbladder removal in a pig using verbal instructions, showcasing progress in autonomous surgical capabilities via imitation learning.

# - **Microsoft's Diagnostic Tool**:
#   - The "Microsoft AI Diagnostic Orchestrator" outperformed doctors by a factor of four in diagnosing complex cases, achieving an 85.5% success rate in tests.    

# - **Qure.AI's IPO Plans**:
#   - Indian healthcare AI startup Qure.AI aims for profitability next year and plans an IPO in two years, focusing on AI tools for early condition detection.      

# - **AI Safety Framework**:
#   - Duke University researchers developed a framework to assess AI safety in healthcare, ensuring accuracy in AI-generated medical notes and responses.

# These highlights demonstrate the ongoing advancements and applications of AI in the healthcare industry.
