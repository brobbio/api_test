from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from src.db import get_db
from src.schemas.user import LoginRequest, LoginResponse
from src.services import auth as user_service

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=LoginResponse)
async def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    """Authenticate a user and return a session token."""
    return user_service.login(credentials.username, credentials.password, db)

