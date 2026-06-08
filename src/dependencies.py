from fastapi import Request, HTTPException, Depends
from src.services.auth import get_current_user

permissions = {
    "maintainer": [
        "items:create",
        "items:read",
        "items:delete"
    ],
    "clerk": [
        "items:read"
    ]
}

def require_auth(request: Request):
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")
    token = auth[len("Bearer "):].strip()
    return get_current_user(token)

def require_permission(permission: str):
    def checker(user=Depends(get_current_user)):
        perms = permissions.get(user["role"], [])

        if permission not in perms:
            raise HTTPException(
                status_code=403,
                detail="Permission denied"
            )

        return user

    return checker