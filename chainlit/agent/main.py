import os
from dotenv import load_dotenv
from typing import cast
import chainlit as cl
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig
import logging

# Setup logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Check if the API key is present
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

@cl.on_chat_start
async def start():
    """Set up the chat session when a user connects."""

    # ✅ Load markdown manually
    try:
        with open("chainlit.md", "r", encoding="utf-8") as f:
            markdown_content = f.read()
        await cl.Message(content=markdown_content).send()
    except FileNotFoundError:
        await cl.Message(content="⚠️ Welcome screen not found. Please add `chainlit.md`.").send()
    except Exception as e:
        await cl.Message(content=f"⚠️ Error loading welcome screen: {str(e)}").send()
        
    # Initialize Gemini client
    external_client = AsyncOpenAI(
        api_key=gemini_api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    )

    # Load the Gemini model
    model = OpenAIChatCompletionsModel(
        model="gemini-2.0-flash",
        openai_client=external_client
    )

    # Configure the agent runner
    config = RunConfig(
        model=model,
        model_provider=external_client,
        tracing_disabled=True
    )

    # Create the health agent
    agent = Agent(
        name="Health Agent",
        instructions="""
            You are a professional health assistant.
            Ask the user how they're feeling, listen to their symptoms,
            and give friendly health advice. Always suggest seeing a real doctor.
        """,
        model=model
    )

    # Store session data
    cl.user_session.set("agent", agent)
    cl.user_session.set("config", config)
    cl.user_session.set("chat_history", [])

    # ✅ Custom chatbot greeting
    await cl.Message(content="👋 Welcome to the Health Assistant! How are you feeling today?").send()

@cl.on_message
async def main(message: cl.Message):
    """Process incoming messages and generate responses."""

    msg = cl.Message(content="Thinking...")
    await msg.send()

    # Retrieve session data
    agent = cast(Agent, cl.user_session.get("agent"))
    config = cast(RunConfig, cl.user_session.get("config"))
    history = cl.user_session.get("chat_history") or []

    # Add user's message to chat history
    history.append({"role": "user", "content": message.content})

    try:
        logger.debug(f"Received user input: {message.content}")
        logger.debug(f"Chat history: {history}")

        # Run agent response
        result = Runner.run_sync(
            starting_agent=agent,
            input=history,
            run_config=config
        )

        # Final response from agent
        response_content = result.final_output
        msg.content = response_content
        await msg.update()

        # Save updated chat history
        cl.user_session.set("chat_history", result.to_input_list())

        logger.info(f"User: {message.content}")
        logger.info(f"Assistant: {response_content}")

    except Exception as e:
        logger.error(f"Error in processing response: {str(e)}")
        msg.content = f"Error: {str(e)}"
        await msg.update()
