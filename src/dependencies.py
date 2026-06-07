from fastapi import Request, HTTPException
from src.services.auth import get_current_user

def require_auth(request: Request):
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")
    token = auth[len("Bearer "):].strip()
    return get_current_user(token)