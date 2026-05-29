import uvicorn
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI(
    title="Test API",
    version="0.0.1"
)

#Fake db
items= {}
next_id = 1

#Fake db schemas
class ItemCreate(BaseModel):
    name: str
    description: Optional[str] = None

 
class ItemResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

#Endpoints
@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.get("/items")
async def read_items():
    """Retrieve every item."""
    return items


@app.get("/items/{item_id}", response_model=ItemResponse)
async def read_item(item_id: int):
    """Retrieve a single item by ID."""
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_id]
 
 
@app.post("/items", response_model=ItemResponse, status_code=201)
async def create_item(item: ItemCreate):
    """Create a new item."""
    global next_id
    new_item = {"id": next_id, "name": item.name, "description": item.description}
    items[next_id] = new_item
    next_id += 1
    return new_item


if __name__ == "__main__":
    uvicorn.run(app, port=8050)