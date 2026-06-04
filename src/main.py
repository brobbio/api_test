import uvicorn
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
import hashlib
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.orm import declarative_base
from src.routers import items, auth

app = FastAPI(
    title="Test API",
    version="0.0.1"
)

app.include_router(auth.router)
app.include_router(items.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# Fake user store
users = {
    "user": hashlib.sha256("password".encode()).hexdigest(),
}

active_tokens = {}  

if __name__ == "__main__":
    uvicorn.run(app, port=8050)