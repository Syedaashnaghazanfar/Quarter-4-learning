# 🧠 Health & Wellness AI Agent


**🔗 [Live App on Streamlit](https://ashnaghazanfar-healthwellness-agent.streamlit.app/)**


A smart, evolving health and wellness assistant built using **Python**, **Streamlit**, and **Gemini API**. This agent is designed to provide users with intelligent, contextual responses related to their health in **JSON format** — ideal for both interaction and tracking over time.

## 🚀 Features

- 🤖 **Conversational Agent**: Interact naturally with an AI that understands and responds to your health and wellness queries.
- 🔍 **Structured JSON Responses**: All insights and recommendations are returned in JSON — ready for tracking, visualization, or integration.
- 📈 **Progress Tracking**: Monitor your wellness journey with historical context and updates.
- 🛠️ **Tools & Handlers**: Utilizes custom tools and handoffs to handle diverse user inputs and maintain modularity.
- 🌐 **Streamlit Interface**: Clean, interactive UI for real-time chat and progress visualization.

> ⚠️ **Note**: This project is under active development. Expect frequent updates and new features like:
> - Personalized wellness plans
> - Habit tracking
> - Visual dashboards
> - OpenAI agents SDK integration

---

## 🧰 Tech Stack

| Tech       | Purpose                              |
|------------|--------------------------------------|
| Python     | Core backend logic                   |
| Streamlit  | Frontend web interface               |
| Gemini API | NLP and intelligent response engine  |
| dotenv     | Env variable management              |
| fpdf / reportlab | PDF export       |
| Custom tools & agents | Specialized handling      |

---

## 🔧 Installation

1. **Clone the repo**:
   ```bash
   git clone https://github.com/syedaashnaghazanfar/health_wellness_agent.git
   cd health_wellness_agent
   ```
2. **Set up your environment**:
 ```bash
   uv venv
   .venv\Scripts\activate
   ```
3.**Install dependencies**:
```bash
uv add -r requirements.txt
```
4.**Create a .env file with your Gemini API key and any other configs**:
```bash
GEMINI_API_KEY=your_api_key_here
```
5.**Run the app**:
```bash
streamlit run main.py
```
## 🛤️ Roadmap

- JSON response framework  
- User session context  
- Streamlit chat interface  
- Progress charts and analytics  
- PDF health summary export  
- Personalized goal tracking  
- AI-powered recommendations    
- Visual dashboards  
- Daily habit streak tracking  
- Natural language input for logging  
- Admin panel for future multi-user support  

---

## 🙌 Contributions

Contributions are welcome! If you have ideas, feedback, or improvements, feel free to fork the repo, submit a pull request, or open an issue. Let’s make something powerful together.

---

## 🧬 License

This project is licensed under the MIT License.

---

Made with ❤️ by Ashna Ghazanfar

   
