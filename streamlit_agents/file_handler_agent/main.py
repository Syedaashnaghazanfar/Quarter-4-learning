import os
import shutil
from pathlib import Path
from agents import Agent, RunContextWrapper, function_tool, Runner
from typing import Optional, Any
import streamlit as st
import asyncio
from dotenv import load_dotenv
import soundfile as sf
from streamlit_mic_recorder import mic_recorder
from openai import OpenAI

# 🌱 Load Environment
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

DESKTOP_PATH = Path(r"D:\code\streamlit_agents")

# 🎯 Tool Functions
@function_tool
async def create_folder(ctx: RunContextWrapper[Any], folder_name: str, directory: Optional[str] = None) -> str:
    try:
        target_dir = Path(directory) if directory else DESKTOP_PATH
        folder_path = target_dir / folder_name
        folder_path.mkdir(exist_ok=True)
        return f"✅ Created folder: {folder_path}"
    except Exception as e:
        return f"❌ Error: {str(e)}"

@function_tool
async def delete_folder(ctx: RunContextWrapper[Any], folder_name: str, directory: Optional[str] = None) -> str:
    try:
        target_dir = Path(directory) if directory else DESKTOP_PATH
        folder_path = target_dir / folder_name
        if not folder_path.exists():
            return f"⚠️ Folder not found: {folder_path}"
        shutil.rmtree(folder_path)
        return f"🗑️ Deleted folder: {folder_path}"
    except Exception as e:
        return f"❌ Error: {str(e)}"

@function_tool
async def list_files(ctx: RunContextWrapper[Any], directory: Optional[str] = None) -> str:
    try:
        target_dir = Path(directory) if directory else DESKTOP_PATH
        contents = [f.name for f in target_dir.iterdir()]
        return "\n".join(contents) or "📂 Directory is empty"
    except Exception as e:
        return f"❌ Error: {str(e)}"

@function_tool
async def read_file(ctx: RunContextWrapper[Any], file_path: str) -> str:
    try:
        full_path = DESKTOP_PATH / file_path
        return full_path.read_text()
    except Exception as e:
        return f"❌ Error: {str(e)}"

@function_tool
async def write_file(ctx: RunContextWrapper[Any], file_path: str, content: str) -> str:
    try:
        full_path = DESKTOP_PATH / file_path
        full_path.write_text(content)
        return f"📝 File saved: {full_path}"
    except Exception as e:
        return f"❌ Error: {str(e)}"

# 🧠 Agents
safety_agent = Agent(
    name="Safety Checker",
    instructions="Check if the input is safe. Reply with 'ALLOW' or 'DENY'.",
)

async def file_safety_guardrail(agent_input):
    result = await Runner.run(safety_agent, input=agent_input)
    decision = result.final_output.strip().upper()
    return decision == "ALLOW"

main_agent = Agent(
    name="File Manager Assistant",
    instructions="Help the user manage files. Use tools to create, delete, list, read, or write files.",
    tools=[create_folder, delete_folder, list_files, read_file, write_file],
)

# 🎛️ Streamlit UI
st.set_page_config(page_title="🎙️ Voice File Manager")
st.title("🧠 File Manager Assistant by Ashna Ghazanfar")
st.markdown("Manage your files **by voice or text**!")

directory_input = st.text_input("📁 Enter directory (optional):", value=str(DESKTOP_PATH))

# 🎤 Voice Input Recorder
audio = mic_recorder(start_prompt="🎙️ Click to Speak", stop_prompt="🛑 Stop", just_once=True, use_container_width=True)

# 🔊 Transcribe Voice if Audio is Present
if audio:
    # Save audio
    audio_path = "temp_input.wav"
    with open(audio_path, "wb") as f:
        f.write(audio["bytes"])

    # Transcribe with OpenAI Whisper
    with open(audio_path, "rb") as f:
        transcript = client.audio.transcriptions.create(model="whisper-1", file=f)
        spoken_text = transcript.text
        st.session_state["user_input"] = spoken_text
        st.success(f"📝 Transcribed: {spoken_text}")

# 💬 Command Input (Auto-filled from voice)
user_input = st.text_input("💬 Your command:", value=st.session_state.get("user_input", ""), key="user_input")

# 🚨 Check for danger
dangerous_keywords = ["delete", "remove", "erase", "destroy"]
is_dangerous = any(word in user_input.lower() for word in dangerous_keywords)

confirm_delete = True
if is_dangerous:
    st.warning("⚠️ This command may delete files.")
    confirm_delete = st.checkbox("✅ I'm sure. Proceed.")

def inject_path(command: str, directory: str) -> str:
    return f"{command} in directory {directory}" if directory else command

# ▶️ Run
if st.button("▶️ Run"):
    if is_dangerous and not confirm_delete:
        st.info("Please confirm before deletion.")
    elif user_input:
        async def run_agent():
            prompt = inject_path(user_input, directory_input)
            if is_dangerous and confirm_delete:
                result = await Runner.run(main_agent, input=prompt)
                return result.final_output
            elif not is_dangerous:
                if await file_safety_guardrail(prompt):
                    result = await Runner.run(main_agent, input=prompt)
                    return result.final_output
                else:
                    return "🚫 Action denied."
            return "🛑 Action not confirmed."

        result = asyncio.run(run_agent())
        st.success(result)
    else:
        st.error("❌ Please say or type a command.")

# 👣 Footer
st.markdown(
    """
    <hr>
    <div style='text-align:center; font-size: 0.9rem;'>
        Built by <strong>Ashna Ghazanfar</strong><br>
        Powered by <em>Streamlit</em> + <em>OpenAI Whisper</em>
    </div>
    """,
    unsafe_allow_html=True
)
