import uvicorn
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from typing import Optional
import hashlib
import secrets

app = FastAPI(
    title="Test API",
    version="0.0.1"
)

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)


#Fake db
items= {}
next_id = 1


# Fake user store
users = {
    "user": hashlib.sha256("password".encode()).hexdigest(),
}
 
active_tokens = {}  


#Requests type classes
class ItemCreate(BaseModel):
    name: str
    description: Optional[str] = None

 
class ItemResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None


class LoginRequest(BaseModel):
    username: str
    password: str
 
 
class LoginResponse(BaseModel):
    token: str
    username: str


#Endpoints

@app.post("/auth/login", response_model=LoginResponse)
async def login(credentials: LoginRequest):
    """Authenticate a user and return a session token."""
    hashed = hashlib.sha256(credentials.password.encode()).hexdigest()
    stored = users.get(credentials.username)
 
    if stored is None or not secrets.compare_digest(stored, hashed):
        raise HTTPException(status_code=401, detail="Invalid credentials")
 
    token = secrets.token_hex(32)
    active_tokens[token] = credentials.username
    return {"token": token, "username": credentials.username}



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