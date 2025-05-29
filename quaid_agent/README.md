# 🧠 Quaid Agent - A Tribute to the Founder 🇵🇰

> _“Expect the best, prepare for the worst.”_  
> — *Quaid-e-Azam Muhammad Ali Jinnah*

---

## 🌟 *About Quaid Agent*

🎉 *This is my **first ever AI Agent project**!*  
**Quaid Agent** is a small, focused AI agent designed to respond to **one specific query**:  
> “Who was Quaid-e-Azam? Give documentary about him.”

It uses **Gemini 2.0 Flash** via **OpenAI's experimental SDK** to deliver a powerful, documentary-style answer about the great leader of Pakistan 🇵🇰

---

## 🧰 *How It Works*

This project:

- Creates an AI agent using the **OpenAI Agents SDK**
- Connects to **Gemini API** via `AsyncOpenAI`
- Asks a predefined question about *Quaid-e-Azam*
- Uses `asyncio` to run the asynchronous tasks cleanly
- Prints out the agent’s final response to the console

---

## 🗂️ *Folder Structure*

```bash
quaid_agent/
├── .env                    # Environment variables (your Gemini API key here), create manually if your cloning!
├── agents.py               # Main Python file (core logic)
├── requirements.txt        # Python dependencies
└── README.md               # This awesome guide you're reading 🌈
```
---
## 🧪 How to Use

✅ *Make sure you're in a **virtual environment** before running!*

---

### 📥 Clone this repo:

```bash
git clone https://github.com/syedaashnaghazanfar/quaid_agent.git
cd quaid_agent
```

### 🛠️ Create your .env file and add your Gemini API key:

```bash
GEMINI_API_KEY=your_api_key_here
```




