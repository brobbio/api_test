import uvicorn
import hashlib
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from pydantic import BaseModel
from sqlalchemy.orm import Session, declarative_base, sessionmaker
from src.routers import items, auth
from src.models import item
from src.models.user import User
from src.db import get_engine, Base, get_db



def seed_users(db: Session):
    users = [
        {
            "username": "user_maintainer",
            "password_hash": hashlib.sha256("maintainer_password".encode()).hexdigest(),
            "role": "maintainer",
        },
        {
            "username": "user_clerk",
            "password_hash": hashlib.sha256("clerk_password".encode()).hexdigest(),
            "role": "clerk",
        },
    ]

    for user_data in users:
        existing = (
            db.query(User)
            .filter(User.username == user_data["username"])
            .first()
        )

        if not existing:
            db.add(User(**user_data))

    db.commit()

# This forces a lazy initialization of the engine db
@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=get_engine())
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=get_engine())
    db = SessionLocal()
    try:
        seed_users(db)
    finally:
        db.close()

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