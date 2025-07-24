# 🧠 Health & Wellness Agent

Your AI-powered companion for improving mental and physical well-being — built using **Gemini**, with modular tools, context memory, guardrails, and real-time streaming.

🌐 **Live Demo**: [Try it on Streamlit](https://health-agent-ashna.streamlit.app/)

---

## 💡 About the Project

The **Health & Wellness Agent** is an interactive AI assistant designed to support users in developing healthier habits, managing wellness routines, and accessing helpful resources. It runs on **Gemini** (Google's cutting-edge language model), wrapped in a thoughtfully structured agent architecture with full support for:

- Custom tools
- Hookable behavior
- Long-term user context
- Live response streaming
- Guardrails & safety checks

---

## ✨ Key Features

| Feature | Description |
|--------|-------------|
| 🧠 **Gemini AI Model** | Powered by Google’s Gemini API for fast, smart, empathetic replies. |
| 🛠️ **Custom Tooling System** | Tools like folder creation, date utilities, and wellness planners modularized for reuse. |
| ⚙️ **Hooks & Lifecycle Events** | Handle custom behavior at run-time, including pre-checks, async side-effects, etc. |
| 📘 **Context Memory** | Remembers user preferences like name, diet, and wellness goals using session-level context management. |
| 🟢 **Streaming Output** | Real-time, token-by-token streaming via a custom `streaming.py` module integrated with Streamlit. |
| 🛡️ **Guardrails** | Safety prompts for risky tasks, permission checks, and clean feedback loops. |
| 💬 **Interactive UI** | Friendly and fast Streamlit-based front-end that feels like chatting with a smart human. |

---

## 🚀 Live App

📲 **Try it now on Streamlit**  
🔗 [https://health-agent-ashna.streamlit.app/](https://health-agent-ashna.streamlit.app/)

---

## 🔧 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Syedaashnaghazanfar/Quarter-4-learning/main/Sir-Aneeq-tasks/task3/health_agent_SDK.git
cd health_agent_SDK
```

### 2. Create and Activate a Virtual Environment using UV

```bash
uv venv
.venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables
Create a .env file in the root directory:

```bash
GEMINI_API_KEY=your_google_gemini_api_key
```

### 5. Run the App

```bash
streamlit run main.py
```

# 🤝 Contributing

We welcome all contributions — whether it’s bug fixes, new tools, UI improvements, or cool feature ideas!

- Fork the repo 🍴  
- Create a branch 🌿  
- Commit your changes ✅  
- Submit a PR 🚀  

Let’s build something beautiful for health & wellness together. 🌼

---

# 📜 License

This project is licensed under the **MIT License**.  
You are free to use, modify, distribute, and even commercialize it — just give credit.

---

**Made with 💚 by Ashna Ghazanfar**
