
# Chat completion api example, it should be reminded what we said so far
# This example uses the OpenAI Python client library to interact with the chat completion API.

from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file
openai_api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role":"user","content":"What's the capital of France?"}],
    #store=True 

)
response2 = client.chat.completions.create(
    model="gpt-4o-mini",
    #previous_response_id=response.id,  -> this would give error because we don't have any argument like this in chat completions
    messages=[{"role":"user","content":"What is the population of that city?"}]
    )

print(response.choices[0].message.content)   # ➜ Paris
print(response2.choices[0].message.content)  # ➜ Could you please specify which city you are referring to? coz it doesn't remember the previous question.

# You bundle the entire conversation history into each request.
# Great when you want full control over memory, ordering, and custom logic.
# We have no build in tools, we have to create our own tools 

# Output:
# The capital of France is Paris.
# Could you please specify which city you are referring to?