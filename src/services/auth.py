from sqlalchemy.orm import Session
from fastapi import HTTPException
import secrets
import hashlib

from src.schemas.user import LoginRequest, LoginResponse

# Fake user store
users = {
    "user": hashlib.sha256("password".encode()).hexdigest(),
}

active_tokens = {}  

def login(username, password):
    hashed = hashlib.sha256(password.encode()).hexdigest()
    stored = users.get(username)
 
    if stored is None or not secrets.compare_digest(stored, hashed):
        raise HTTPException(status_code=401, detail="Invalid credentials")
 
    token = secrets.token_hex(32)
    active_tokens[token] = username
    return {"token": token, "username": username}

def logout(token):
    auth = request.headers.get("Authorization", "")
    if auth.startswith("Bearer "):
        token = auth[len("Bearer "):].strip()
        
    if token not in active_tokens:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    del active_tokens[token]