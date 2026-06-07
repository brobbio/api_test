import uvicorn
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
import hashlib
from contextlib import asynccontextmanager
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.orm import declarative_base
from src.routers import items, auth
from src.models import item
from src.db import get_engine, Base

# This forces a lazy initialization of the engine db
@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=get_engine())
    yield

app = FastAPI(
    title="Test API",
    version="0.0.1",
    lifespan=lifespan
)

app.include_router(auth.router)
app.include_router(items.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(app, port=8050)