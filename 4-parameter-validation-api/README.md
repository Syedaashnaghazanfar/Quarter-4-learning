# 🎯 FastAPI Parameter Validation Learning

## 📚 Overview  
This project demonstrates how to validate different types of parameters in FastAPI, including **path parameters**, **query parameters**, and **request bodies**.  
It's a practical guide for building robust APIs with clear validation rules and helpful error messages.

---

## 📝 Related Blog Post  
Check out my detailed blog post on API Parameters in FastAPI:  
[API Parameters in FastAPI: The Ultimate Guide](https://your-blog-link-here)  *(Replace with your actual URL)*

---

## 🔍 Features Implemented  

1. **Path Parameters**  
   - Basic validation  
   - Numeric constraints (`ge`, `le`)  
   - Required parameters  
   - Example endpoint: `/items/{item_id}`

2. **Query Parameters**  
   - Optional and required parameters  
   - String length validation (`min_length`, `max_length`)  
   - Numeric range validation  
   - Multiple query parameters  
   - Example endpoint: `/search/?q=phone&skip=0&limit=10`

3. **Request Body**  
   - Pydantic model validation  
   - Optional fields  
   - Type validation  
   - Example payloads included

4. **Combined Parameters**  
   - Mix of Path + Query + Body  
   - Complex validation scenarios  
   - Error handling examples

---

## 📝 API Endpoints

| Endpoint                    | Method | Description                               |
|-----------------------------|--------|-------------------------------------------|
| `/items/{item_id}`          | GET    | Path parameter validation, integer ≥ 1   |
| `/search/`                  | GET    | Multiple query parameters with validation|
| `/items/{item_id}`          | PUT    | Combine path, query & request body params|
| `/filter/`                  | GET    | List parameters and price range filtering|
| `/items/{item_id}/validate` | GET    | Custom validation logic with strict mode |

---

## 🤝 Contact

**Ashna Ghazanfar**  
✉️ ashna@example.com  
🔗 [LinkedIn Profile](https://www.linkedin.com/in/ashna-ghazanfar-b268522b4/)

---

*Created with 💖 by Ashna Ghazanfar*
