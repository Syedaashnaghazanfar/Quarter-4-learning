from fastapi import FastAPI
from typing import Optional

app = FastAPI()

@app.get("/")
def read_root(name: Optional[str] = "Guest"):  #an optional query parameter for name its default value is "Guest" (extra work)

    return {"message": f"Hello {name}! Welcome to the FastAPI project by Ashna!"}

@app.get("/items/{item_id}") # path parameter| ye kisi bhi naam se ho sakta hai jo hum url par pass karte hain and we get our value in the function
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q} # here q is an optional query parameter
