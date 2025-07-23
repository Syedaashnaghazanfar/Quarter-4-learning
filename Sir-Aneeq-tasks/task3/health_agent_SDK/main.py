# main.py
import streamlit as st
import asyncio

from context import get_user_context
from streaming import stream_agent_response

# Page Configuration
st.set_page_config(
    page_title="🧠 Health & Wellness Planner AI",
    page_icon="💪",
    layout="wide"
)

# Sidebar Content
with st.sidebar:
    st.title("💚 Your Wellness Sidekick")
    st.markdown("""
    Welcome **Ashna!**  
    I'm your AI-powered assistant here to help with:
    
    - 🥗 Nutrition & meal planning  
    - 🏋️ Personalized workouts  
    - 🧘‍♀️ Stress management  
    - ⏰ Scheduling routines  
    
    Let’s build the best version of you — one healthy step at a time. 🌿
    """)
    st.info("Go ahead, ask me anything!")

# Main Chat UI
st.title("🧬 Health & Wellness Planner AI")
st.write(
    "I'm your personal **health and wellness assistant** 🤖. "
    "Ask me anything from fitness tips to mental wellness advice!"
)

# Chat input from user
user_input = st.chat_input("What's on your mind today?")

# User context initialization
if "context" not in st.session_state:
    st.session_state.context = get_user_context("Ashna Ghazanfar", 1)

# Handle user question
if user_input:
    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        placeholder = st.empty()

        async def run_stream():
            output_text = ""
            async for token in stream_agent_response(user_input, st.session_state.context):
                output_text += token
                placeholder.markdown(output_text)

        # Safely run asyncio in Streamlit
        try:
            asyncio.run(run_stream())
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(run_stream())
