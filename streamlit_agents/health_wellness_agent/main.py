import streamlit as st
from dotenv import load_dotenv
from datetime import datetime
import random
import pandas as pd
from agent import HealthWellnessAgent
from context import UserSessionContext, RunContextWrapper
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import tempfile
import re

# Load environment variables
load_dotenv()

# Daily Tips
DAILY_TIPS = [
    "🌼 Start your day with a glass of water and deep breaths",
    "🧘‍♀️ Take 5 minutes to stretch and relax your mind",
    "🌙 Aim for 7-9 hours of quality sleep tonight",
    "🚶‍♂️ A short walk can boost your mood and energy",
    "💨 Practice mindful breathing when feeling stressed",
    "🍎 Add an extra serving of vegetables to your meals today",
    "📱 Take regular breaks from screens to rest your eyes",
    "💪 Celebrate small victories - they add up to big results",
    "😊 Share a smile - it's contagious!"
]

# Initialize session state
def initialize_session_state():
    if 'agent' not in st.session_state:
        st.session_state.agent = HealthWellnessAgent()
    
    if 'context' not in st.session_state:
        st.session_state.context = RunContextWrapper(UserSessionContext(name="", uid=random.randint(1000, 9999)))
    
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    if 'user_profile' not in st.session_state:
        st.session_state.user_profile = {
            'name': '',
            'age': 30,
            'weight': 70,
            'height': 170,
            'bmi': 0,
            'goal': '',
            'last_update': ''
        }
    
    if 'habits' not in st.session_state:
        st.session_state.habits = [
            {'name': 'Drink 8 glasses of water 💧', 'done': False},
            {'name': 'Walk 10,000 steps 🚶‍♀️', 'done': False},
            {'name': 'Eat 5 servings of veggies 🥦', 'done': False},
            {'name': 'Focus on deep breathing 🌬️', 'done': False},
        ]
    
    if 'mood_logs' not in st.session_state:
        st.session_state.mood_logs = []

# Calculate BMI
def calculate_bmi(weight, height):
    if height == 0:
        return 0
    return round(weight / ((height / 100) ** 2), 1)

def remove_emojis(text):
    emoji_pattern = re.compile(
        "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport
        u"\U0001F1E0-\U0001F1FF"  # flags
        u"\U00002700-\U000027BF"
        u"\U0001F900-\U0001F9FF"
        u"\U0001FA70-\U0001FAFF"
        u"\u200d"
        u"\u2640-\u2642"
        "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)

def generate_pdf():
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='SectionHeader', fontSize=14, spaceAfter=10, leading=18, fontName='Helvetica-Bold'))
    styles.add(ParagraphStyle(name='NormalText', fontSize=11, spaceAfter=6, leading=14, fontName='Helvetica'))

    story = []

    def add_section(title, lines):
        story.append(Paragraph(remove_emojis(title), styles['SectionHeader']))
        for line in lines:
            story.append(Paragraph(remove_emojis(str(line)), styles['NormalText']))
        story.append(Spacer(1, 12))

    # Title
    story.append(Paragraph("Your Wellness Report", styles['Title']))
    story.append(Spacer(1, 16))

    # Profile
    profile = st.session_state.user_profile
    profile_lines = [f"{key.capitalize()}: {profile[key]}" for key in ['name', 'age', 'weight', 'height', 'bmi', 'goal']]
    add_section("👤 Personal Profile", profile_lines)

    # Habits
    habit_lines = [f"{'DONE' if h['done'] else 'PENDING'} - {h['name']}" for h in st.session_state.habits]
    add_section("✅ Habit Tracker", habit_lines)

    # Mood
    if st.session_state.mood_logs:
        mood_lines = [f"{log['date']}: {log['mood']} (Energy: {log['energy']}/10)" for log in st.session_state.mood_logs[-5:]]
        add_section("😊 Mood History", mood_lines)

    # Chat
    if st.session_state.messages:
        chat_lines = [f"{'You' if m['role']=='user' else 'Assistant'}: {m['content']}" for m in st.session_state.messages[-5:]]
        add_section("💬 Chat Highlights", chat_lines)

    # Tips
    tip_lines = [f"- {tip}" for tip in random.sample(DAILY_TIPS, 3)]
    add_section("💡 Personalized Tips", tip_lines)

    # Save PDF
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
    doc = SimpleDocTemplate(temp_file.name, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    doc.build(story)

    return temp_file.name

# Main App
def main():
    st.set_page_config(page_title="Health & Wellness Companion", page_icon="🌸", layout="wide")
    initialize_session_state()
    
    # Title
    st.title("🌸 Your Health & Wellness Companion")
    st.markdown("Your personalized guide to better health and wellbeing")
    
    # Sidebar - User Profile
    with st.sidebar:
        st.header("Your Profile")
        
        with st.form("user_profile_form"):
            name = st.text_input("Name", value=st.session_state.user_profile['name'])
            age = st.number_input("Age", min_value=1, max_value=120, value=st.session_state.user_profile['age'])
            weight = st.number_input("Weight (kg)", min_value=30, max_value=200, value=st.session_state.user_profile['weight'])
            height = st.number_input("Height (cm)", min_value=100, max_value=250, value=st.session_state.user_profile['height'])
           
            
            if st.form_submit_button("Update Profile"):
                st.session_state.user_profile = {
                    'name': name,
                    'age': age,
                    'weight': weight,
                    'height': height,
                    'bmi': calculate_bmi(weight, height),
                    'goal': st.session_state.user_profile['goal'],  # Keep existing goal
                    'last_update': datetime.now().strftime("%Y-%m-%d")
                }
                st.session_state.context.update_context(name=name)
                st.success("Profile updated!")
        
        st.divider()
        
        # Health Stats
        st.header("📊 Your Stats")
        st.metric("BMI", st.session_state.user_profile['bmi'])
        
        # Progress
        completed_habits = sum(1 for h in st.session_state.habits if h['done'])
        st.metric("Daily Habits", f"{completed_habits}/{len(st.session_state.habits)}")
        
        # Mood History
        if st.session_state.mood_logs:
            latest_mood = st.session_state.mood_logs[-1]['mood']
            st.metric("Recent Mood", latest_mood.split()[0])  # Just the emoji
        
        st.divider()
        
        # Daily Tip
        st.header("💡 Daily Tip")
        st.info(random.choice(DAILY_TIPS))
        st.session_state.context.update_context(daily_tip=random.choice(DAILY_TIPS))

         # Divider
        st.divider()
        
        
        # Last Update
        st.subheader("Last Updated")
        last_update = st.session_state.user_profile['last_update']
        if last_update:
            st.write(f"Your profile was last updated on: {last_update}")
        else:
            st.write("Your profile has not been updated yet.")
        # Divider
        st.divider()

        # Goal Setting
        st.header("🎯 Set Your Wellness Goal")
        goal_text = st.text_input("What is your main wellness goal?", value=st.session_state.user_profile['goal'])
        if st.button("Set Goal"):
            if goal_text:
                st.session_state.user_profile['goal'] = goal_text
                st.session_state.context.update_context(goal=goal_text)
                st.success("Goal set successfully!")
            else:
                st.error("Please enter a valid goal.")
     
        
        # PDF Download
        st.divider()
        if st.button("📄 Download Wellness Report"):
            pdf_path = generate_pdf()
            with open(pdf_path, "rb") as f:
                st.download_button(
                    label="⬇️ Save as PDF",
                    data=f,
                    file_name="wellness_report.pdf",
                    mime="application/pdf"
                )
    
    # Main Content Tabs
    tab1, tab2, tab3 = st.tabs(["💬 Chat", "📝 Habits & Mood", "📈 Insights"])
    
    with tab1:
        st.header("💬 Chat with Your Wellness Companion")
        
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])
        
        # Chat input
        if prompt := st.chat_input("How can I help you today?"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            with st.chat_message("user"):
                st.write(prompt)
            
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        response = st.session_state.agent.process_message(prompt, st.session_state.context)
                        if response['response_type'] == 'error':
                            st.error(f"Oops: {response['content']['error']}")
                        else:
                            content = response['content']
                            st.write(content)
                            st.session_state.messages.append({"role": "assistant", "content": str(content)})
                    except Exception as e:
                        st.error(f"Something went wrong: {str(e)}")
    
    with tab2:
        st.header("📝 Track Your Daily Habits")
        
        # Habit Tracker
        st.subheader("✅ Today's Habits")
        for i, habit in enumerate(st.session_state.habits):
            cols = st.columns([4, 1])
            with cols[0]:
                st.write(habit['name'])
            with cols[1]:
                st.session_state.habits[i]['done'] = st.checkbox(
                    "Done", 
                    value=habit['done'], 
                    key=f"habit_{i}",
                    label_visibility="collapsed"
                )
        
        # Add new habit
        new_habit = st.text_input("Add a new habit", key="new_habit")
        if st.button("Add Habit") and new_habit:
            st.session_state.habits.append({'name': new_habit, 'done': False})
            st.rerun()
        
        # Mood Tracker
        st.subheader("😊 Daily Mood Check")
        with st.form("mood_form"):
            mood = st.selectbox(
                "How are you feeling today?",
                ["😀 Excellent", "🙂 Good", "😐 Neutral", "🙁 Tired", "😞 Down", "😡 Frustrated"]
            )
            energy = st.slider("Energy Level (1-10)", 1, 10, 5)
            notes = st.text_area("Any notes about your day")
            
            if st.form_submit_button("Log My Mood"):
                st.session_state.mood_logs.append({
                    'date': datetime.now().strftime('%Y-%m-%d %H:%M'),
                    'mood': mood,
                    'energy': energy,
                    'notes': notes
                })
                st.success("Mood logged successfully!")
    
    with tab3:
        st.header("📈 Your Wellness Insights")
        
        if not st.session_state.user_profile['name']:
            st.info("Complete your profile in the sidebar to see personalized insights")
        else:
            # Health Summary
            st.subheader("� Health Summary")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Age", st.session_state.user_profile['age'])
            with col2:
                st.metric("Weight", f"{st.session_state.user_profile['weight']} kg")
            with col3:
                st.metric("BMI", st.session_state.user_profile['bmi'])
            
            # Habit Completion
            st.subheader("📊 Habit Completion")
            habit_df = pd.DataFrame(st.session_state.habits)
            st.bar_chart(habit_df['name'].value_counts())
            
            # Mood History
            if st.session_state.mood_logs:
                st.subheader("😊 Mood History")
                mood_df = pd.DataFrame(st.session_state.mood_logs)
                st.line_chart(mood_df.set_index('date')['energy'])
                
                with st.expander("View Mood Logs"):
                    st.dataframe(mood_df[['date', 'mood', 'energy']])
            
            # Chat Analysis
            if st.session_state.messages:
                st.subheader("💬 Chat Topics")
                messages_text = " ".join([msg['content'] for msg in st.session_state.messages])
                st.write("Recent topics discussed:")
                st.write(messages_text[:500] + "...")  # Show first 500 chars

if __name__ == "__main__":
    main()































