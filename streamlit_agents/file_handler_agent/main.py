import os
import shutil
from pathlib import Path
from agents import Agent, FunctionTool, RunContextWrapper, function_tool, Runner
from typing import Optional, Any
import streamlit as st
import asyncio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Define your specific desktop path
DESKTOP_PATH = Path(r"D:\code\streamlit_agents")

# --- File Management Tools ---
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

# --- Safety Agent (Guardrails) ---
safety_agent = Agent(
    name="Safety Checker",
    instructions="You check if the user input is safe to run. Reply ONLY with 'ALLOW' or 'DENY'.",
)

async def file_safety_guardrail(agent_input):
    result = await Runner.run(safety_agent, input=agent_input)
    decision = result.final_output.strip().upper()
    return decision == "ALLOW"

# --- Main Agent ---
main_agent = Agent(
    name="File Manager Assistant",
    instructions=(
        "You help users manage files and folders using tools. "
        "Just do what the user asks using available tools. "
        "You're allowed to create, delete, read, and write files."
    ),
    tools=[create_folder, delete_folder, list_files, read_file, write_file],
)

# --- Streamlit UI ---
st.set_page_config(page_title="📁 File Manager Assistant")
st.title("🧠 File Manager Assistant By Ashna Ghazanfar")

st.markdown("Manage your files using natural language. AI will handle the commands below:")

# 🔹 Let user optionally specify a custom path
directory_input = st.text_input("🔍 Enter directory path (optional):", value=str(DESKTOP_PATH))

st.info(
    f"""
    **📝 Note:**  
    • If you don't enter a directory, the default path will be: `{DESKTOP_PATH}`  
    • Make sure your folder or file names go inside this path.  
    • Example (no path): `create a folder named test_folder`  
    • Example (with path): `create folder test_folder in directory D:\\\\myfiles`
    """
)

user_input = st.text_input("💬 Enter your instruction:")

# 🚨 Detect dangerous commands
dangerous_keywords = ["delete", "remove", "erase", "destroy"]
is_dangerous = any(word in user_input.lower() for word in dangerous_keywords)

confirm_delete = True
if is_dangerous:
    st.warning("⚠️ This command may delete files or folders.")
    confirm_delete = st.checkbox("✅ I'm sure. Proceed with deletion.")

# 🧠 Inject directory into command
def inject_path_into_input(command: str, directory: str) -> str:
    return f"{command} in directory {directory}" if directory else command

# ▶️ Run Command Button
if st.button("▶️ Run Command"):
    if is_dangerous and not confirm_delete:
        st.info("🛑 Please confirm you're sure before running this destructive command.")
    elif user_input:
        async def run_agent():
            prompt = inject_path_into_input(user_input, directory_input)

            if is_dangerous and confirm_delete:
                result = await Runner.run(main_agent, input=prompt)
                return result.final_output
            elif not is_dangerous:
                if await file_safety_guardrail(prompt):
                    result = await Runner.run(main_agent, input=prompt)
                    return result.final_output
                else:
                    return "🚫 Action denied by Safety Checker."
            else:
                return "🛑 Action not confirmed."

        output = asyncio.run(run_agent())
        st.success(output)
    else:
        st.error("❌ Please enter a command to run.")

# --- Footer ---
st.markdown(
    """
    <hr style='margin-top:30px; margin-bottom:10px'>
    <div style='text-align:center; font-size: 0.9rem;'>
        Created by <strong>Ashna Ghazanfar</strong><br>
        Powered by <em>Streamlit</em> and <em>OpenAI Agents SDK</em>
    </div>
    """,
    unsafe_allow_html=True
)
