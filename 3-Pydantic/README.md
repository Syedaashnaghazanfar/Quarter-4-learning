# 🚀 Learning Pydantic: Data Validation  
_A project demonstrating Python data validation with Pydantic and FastAPI._  

---

## 📚 **Overview**  
This repository documents my exploration of **Pydantic**, showcasing how it enforces type safety and data integrity through practical examples.

---

## 📝 **Related Blog Post**  
[**Pydantic: The Elegant Guardian of Python Data**](https://your-blog-url-here.com)  

---

## 🌟 **Core Concepts & Code Examples**

### 1. **Basic Model Definition**
```python
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    email: str
    age: int | None = None  # Optional field
2. 🏗️ Nested Models
python
class Address(BaseModel):
    street: str
    city: str
    zip_code: str

class UserWithAddress(BaseModel):
    name: str
    addresses: list[Address]
3. ✨ Custom Validation
python
from pydantic import validator

class Product(BaseModel):
    name: str
    price: float
    
    @validator('price')
    def price_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("Price must be positive")
        return v
4. 🛠️ FastAPI Integration
python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Message(BaseModel):
    text: str

class Response(BaseModel):
    reply: str

@app.post("/chat/", response_model=Response)
async def chat(message: Message):
    if not message.text.strip():
        raise HTTPException(status_code=400, detail="Empty message")
    return Response(reply="Processed: " + message.text)
🔍 Project Structure
File	Description
pydantic_example_1.py	Basic model validation
pydantic_example_2.py	Nested models demo
pydantic_example_3.py	Custom validators implementation
main.py	Complete FastAPI application
🚀 Quick Start
Prerequisites
Python 3.8+

pip package manager

Installation
bash
# Create virtual environment
python -m venv .venv

# Activate environment
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Install dependencies
pip install "fastapi[all]" pydantic email-validator
Running Examples
bash
# Basic validation demo
python pydantic_example_1.py

# Start FastAPI server
uvicorn main:app --reload
💡 Key Features
✅ Type Enforcement: Automatic data type validation

✅ Error Reporting: Detailed validation errors

✅ Nested Models: Support for complex data structures

✅ Serialization: Easy JSON conversion

✅ API Integration: Seamless FastAPI compatibility

🌟 Learning Outcomes
Creating data models with strict type constraints

Implementing hierarchical/nested data validation

Developing custom validation rules

Building REST APIs with automatic request validation

Handling validation errors effectively

Serializing models to/from JSON

