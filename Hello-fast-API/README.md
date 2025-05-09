# 🚀 FastDCA P1 – Hello World with FastAPI + UV

> _My first FastAPI project setup using uv, showcasing a basic API with two routes and modern Python practices 🐍✨_

---

## 📌 What is FastAPI?

**FastAPI** is a **modern, high-performance** web framework for building APIs with Python based on standard Python type hints. It gives you:

- ⚡ Automatic interactive docs (Swagger & ReDoc)
- 🔐 Built-in validation and error handling
- 🧠 Type-safe and minimal boilerplate
- 🚀 Super fast thanks to ASGI

---

## 📦 What is UV?

**uv** is a **fast Python package and environment manager** built in Rust. It replaces pip + venv with one tool. Think of it like yarn or bun for Python:

- 🧊 Manages virtual environments
- ⚡ Super fast dependency installs
- 📁 Uses `pyproject.toml` instead of `requirements.txt`
- 🛠️ Handles dev dependencies cleanly

---
## 🧾 My Learnings

- 💡 How to **scaffold a FastAPI project** with `uv`
- 🔍 The difference between **path parameters** and **query parameters**
- 🔌 Running ASGI apps using **Uvicorn**
- 📑 Accessing **interactive API docs instantly** at `/docs` and `/redoc`
- 🧰 Handling **basic errors and PowerShell permission issues** on Windows 😅

---

## 🛠️ Tools & Tech Stack

- `FastAPI` – Modern Python web framework
- `uv` – Fast dependency + environment manager
- `Uvicorn` – ASGI server


---

## 🔗 API Endpoints

| Method | Path                  | Description                             |
|--------|-----------------------|-----------------------------------------|
| GET    | `/`                   | Returns: `{"message":"Hello Guest! Welcome to the FastAPI project by Ashna!"}`           |
| GET    | `/?name=Fatima`       | Returns: `{"message":"Hello Fatima! Welcome to the FastAPI project by Ashna!"}`           |
| GET    | `/items/{item_id}`    | Returns: dynamic `item_id` and `q`      |


> ✨ This is **Task 2** for **Quarter 4**, built using **FastAPI** and managed with **uv**.

📌 *Created with 💻 by* ***Ashna Ghazanfar***
