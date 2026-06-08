import jwt
import secrets
import hashlib
import os
from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime, timedelta
from src.schemas.user import LoginRequest, LoginResponse
from src.models.user import User

# Fake user store
users = {
    "user": hashlib.sha256("password".encode()).hexdigest(),
}

active_tokens = {}  

SECRET = os.getenv("JWT_SECRET")

def get_user_role(username: str, db: Session):
    return (
        db.query(User)
        .filter(User.username == username)
        .first()
    )

def login(username, password, db):
    hashed = hashlib.sha256(password.encode()).hexdigest()
    stored = users.get(username)
 
    if stored is None or not secrets.compare_digest(stored, hashed):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    role = get_user_role(username, db)
 
    if role is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    payload = {"sub": username, "role": role ,"exp": datetime.utcnow() + timedelta(hours=1)}
    token = jwt.encode(payload, SECRET, algorithm="HS256")
    return {"token": token, "username": username}


def get_current_user(token):
    try:
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
        return payload["sub"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

def logout(token):
    auth = request.headers.get("Authorization", "")
    if auth.startswith("Bearer "):
        token = auth[len("Bearer "):].strip()
        
    if token not in active_tokens:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    del active_tokens[token]