import uvicorn
from fastapi import FastAPI, Request, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
import hashlib
import secrets
from sqlalchemy.orm import Session
from sqlalchemy.orm import declarative_base

Base = declarative_base()


from repository import insert_item, save_db
from db import get_engine, SessionLocal, get_db, engine
from models import ItemsData

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



@app.delete("/auth/logout", status_code=204)
async def logout(request: Request):
    """Invalidate the current session token."""
    auth = request.headers.get("Authorization", "")
    if auth.startswith("Bearer "):
        token = auth[len("Bearer "):].strip()
        
    if token not in active_tokens:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    del active_tokens[token]


@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.get("/items")
async def read_items(
    limit: int = 10,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """Retrieve every item."""
    return (
        db.query(ItemsData)
        .offset(offset)
        .limit(limit)
        .all()
    )


@app.get("/items/{item_id}", response_model=ItemResponse)
async def read_item(item_id: int, db: Session = Depends(get_db)):
    """Retrieve a single item by ID."""
    item = (
        db.query(ItemsData)
        .filter(ItemsData.id == item_id)
        .first()
    )

    if item is None:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )

    return item
 
 
@app.post("/items", response_model=ItemResponse, status_code=201)
async def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    """Create a new item."""
    new_item = ItemsData(name=item.name, description=item.description)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    
    return new_item


if __name__ == "__main__":
    uvicorn.run(app, port=8050)