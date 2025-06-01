import os
from agents import (
    Agent,
    Runner,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    set_tracing_disabled,
    function_tool,
)
from dotenv import load_dotenv
from agents.run import RunConfig
import math

# 🌿 Load environment variables
# Yeh line environment variables ko load karti hai (.env file se).
load_dotenv()
# 🌿 Disable tracing (agar debugging ka scene nahi chahiye)
set_tracing_disabled(disabled=True)

# 🌿 API key uthao environment variables se
OPEN_ROUTER_API_KEY = os.getenv("OPEN_ROUTER_API_KEY")
if not OPEN_ROUTER_API_KEY:
    raise ValueError("OPEN_ROUTER_API_KEY not found in environment variables")  # Agar key missing ho, to error do

# 🌿 Yeh external_client, OpenRouter ke liye aik client create karta hai.
# Samajh lo ke OpenRouter aik behtar router hai jo APIs ke traffic ko manage karta hai.
external_client = AsyncOpenAI(
    api_key=OPEN_ROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",  # Yeh OpenRouter ka API endpoint hai.
)

# 🌿 Yeh model define kar raha hai (OpenRouter ke through LLaMA-3 model ko istemal karte hue)
model = OpenAIChatCompletionsModel(
    model="meta-llama/llama-3-70b-instruct",  # Yeh specific LLM ka naam hai.
    openai_client=external_client,
)

# 🌿 RunConfig aik config object hai jo batata hai kaisa model aur provider use hoga
config = RunConfig(
    model=model,
    model_provider=external_client,
)

# 🌿 Neeche kuch mathematical tools banaye gaye hain. Har aik tool aik asynchronous function hai.
# Matlab ye functions wait karte hain jab tak kaam mukammal nahi hota (non-blocking code likhne ka tareeqa).

@function_tool
async def add(a: float, b: float) -> float:
    # Do numbers ka sum karo
    return a + b

@function_tool
async def subtract(a: float, b: float) -> float:
    # Do numbers ka difference nikaalo
    return a - b

@function_tool
async def multiply(a: float, b: float) -> float:
    # Do numbers ko multiply karo
    return a * b

@function_tool
async def divide(a: float, b: float) -> float:
    # Divide karte hue check karo ke denominator zero na ho!
    if b == 0:
        raise ValueError("Division by zero is not allowed")
    return a / b

# 🌿 Kuch scientific functions bhi hain
@function_tool
async def square_root(x: float) -> float:
    # Negative number ka square root nahi nikal sakte
    if x < 0:
        raise ValueError("Cannot take square root of a negative number")
    return math.sqrt(x)

@function_tool
async def power(base: float, exponent: float) -> float:
    # Exponentiation (base raised to power exponent)
    return math.pow(base, exponent)

@function_tool
async def logarithm(x: float, base: float = math.e) -> float:
    # Logarithm function, default base e (natural log)
    if x <= 0:
        raise ValueError("Logarithm input must be positive")
    return math.log(x, base)

@function_tool
async def sine(angle_degrees: float) -> float:
    # Sine function, angle degrees mein diya gaya hai
    return math.sin(math.radians(angle_degrees))

@function_tool
async def cosine(angle_degrees: float) -> float:
    # Cosine function, angle degrees mein diya gaya hai
    return math.cos(math.radians(angle_degrees))

@function_tool
async def tangent(angle_degrees: float) -> float:
    # Tangent function, angle degrees mein diya gaya hai
    return math.tan(math.radians(angle_degrees))

@function_tool
async def factorial(n: int) -> int:
    # Factorial nikalna hai, negative number allowed nahi hai
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    return math.factorial(n)

# 🌿 Yeh aik Scientific Calculator Agent bana raha hai.
# Samajh lo yeh aik virtual calculator hai jo har tarah ke sawalon ka jawab de sakta hai.
agent = Agent(
    name="ScientificCalculatorAgent",
    instructions="You are a smart scientific calculator. Use the tools to perform operations based on the user's queries.",
    tools=[add, subtract, multiply, divide, square_root, power, logarithm, sine, cosine, tangent, factorial]
)

# 🌿 Yeh kuch queries hain jo test ke liye diye gaye hain.
queries = [
    "What is 25 + 17?",  # Basic addition
    "Calculate the square root of 144",  # Square root test
    "What is 2 raised to the power of 5?",  # Power calculation
    "Find log base 10 of 1000",  # Logarithm calculation
    "What is the sine of 30 degrees?",  # Sine function
    "Compute 5 factorial",  # Factorial test
    "Divide 100 by 25"  # Division test
]

# 🌿 Yeh loop har query ko agent ke zariye run karta hai aur result print karta hai.
for query in queries:
    # Yeh line synchronous run karti hai, yani aik waqt mein aik kaam
    result = Runner.run_sync(agent, query, run_config=config)
    # Final result print karo!
    print(f"Query: {query} -> Result: {result.final_output}")

# 🌟🌟🌟
# Summary of the Urdu-Style Notes:
# - Yeh program aik scientific calculator agent banata hai jo OpenRouter API ko use karta hai.
# - Sirf aik endpoint ka use hota hai (https://openrouter.ai/api/v1), aur woh automatically best model ko connect karta hai.
# - Tumhein multiple API endpoints ke chakkar mein nahi padna padta. Bas aik hi API key, aik endpoint – sab kaam ho jata hai.
# - Yeh example practical hai, real-world usage ka behtareen misal hai.
