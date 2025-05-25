from fastapi import FastAPI, Query, Path, Body
from pydantic import BaseModel
from typing import List, Tuple, Optional

# 🛠️ Initialize the FastAPI app with metadata (useful for Swagger docs)
app = FastAPI(
    title="Parameter Validation API",
    description="An API demonstrating how to validate path, query, and body parameters using FastAPI",
    version="1.0.0",
    contact={
        "name": "Ashna Ghazanfar",
        "email": "ashna@example.com",
    },
)

# 🏠 Root endpoint – just a basic welcome
@app.get("/")
def read_root():
    return {"message": "Welcome to the Parameter Validation API"}

# 📦 Pydantic model to define the structure of an item (body data)
class Item(BaseModel):
    name: str
    description: Optional[str] = None  # Optional field
    price: float
    is_offer: Optional[bool] = None  # Optional field

# 🔍 Example of a simple path parameter
@app.get("/items/{item_id}")
def read_item(item_id: int = Path(..., title="The ID of the item", ge=1)):
    # item_id must be an integer ≥ 1
    return {"item_id": item_id, "message": f"You requested item #{item_id}"}

# 🔎 Example of multiple query parameters
@app.get("/search/")
def search_items(
    q: Optional[str] = Query(None, min_length=3, max_length=50, title="Search query"),
    category: Optional[str] = Query(None, title="Item category"),
    skip: int = Query(0, ge=0, title="Items to skip"),
    limit: int = Query(10, le=100, title="Maximum items to return"),
):
    # Build a response showing what the user searched for
    return {
        "query": q,
        "category": category,
        "skip": skip,
        "limit": limit,
        "message": "Search results filtered successfully"
    }

# 📬 Combine all 3 types of parameters: path, query, and body
@app.put("/items/{item_id}")
def update_item(
    item_id: int = Path(..., title="ID of the item to update", ge=1),
    q: Optional[str] = Query(None, title="Optional query string"),
    item: Item = Body(...),  # Full item data from request body
):
    # Return all received info in a neat JSON
    return {
        "item_id": item_id,
        "query": q,
        "item": item
    }

# 📂 List and Tuple query parameters (like filters)
@app.get("/filter/")
def filter_items(
    categories: List[str] = Query(..., title="Filter by categories"),
    price_range: Tuple[float, float] = Query(..., title="Price range (min, max)")
):
    # Show what the user filtered for
    return {
        "categories": categories,
        "price_range": price_range,
        "message": "Filtered items by category and price range"
    }

# ⚠️ Parameter validation with custom logic
@app.get("/items/{item_id}/validate")
def validate_item(
    item_id: int = Path(..., ge=1, title="Item ID (must be >= 1)"),
    strict: bool = Query(False, title="Enable strict mode")  # default is False
):
    # Custom rule: if strict mode is on, item_id must not be > 100
    if strict and item_id > 100:
        return {"error": "Item ID cannot be greater than 100 in strict mode"}
    
    # Otherwise, it's valid
    return {
        "item_id": item_id,
        "strict_mode": strict,
        "message": "Item ID is valid"
    }
# 📝 Run the app with: uvicorn main:app --reload