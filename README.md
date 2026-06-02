# Items App

A simple full-stack items storage/retrieval web app with a FastAPI backend and a Vue.js frontend.

## Stack

- **Backend**: FastAPI + PyJWT
- **Frontend**: Vue 3 (CDN, no build step)

## Project structure

```
├── main.py           # FastAPI app
├── auth.js           # Shared auth logic (token storage, logout)
├── index.html        # Main page (add and look up items)
├── app.js
├── style.css
├── login.html        # Login page
├── login.js
├── login.css
├── test_unit.py      # Unit tests (no server needed)
├── test_integration.py
└── requirements.txt
```

## Setup

```bash
pip install -r requirements.txt
```

## Running

```bash
# Start the backend
uvicorn main:app --reload

# Open the frontend
# Serve index.html on port 5500 (e.g. VS Code Live Server)
```

API docs available at `http://localhost:8000/docs`.

## API endpoints

| Method | Path | Description |
|---|---|---|
| `POST` | `/auth/login` | Login, returns a JWT |
| `DELETE` | `/auth/logout` | Logout (validates token) |
| `GET` | `/items/{id}` | Get an item by ID |
| `POST` | `/items` | Create an item |

## Auth

JWT-based. Tokens expire after **1 hour**. On login the token is stored in `localStorage` and sent as `Authorization: Bearer <token>` on subsequent requests.

> **Note**: logout does not invalidate the token server-side — it will remain valid until expiry. A denylist is needed for true invalidation.

## Test users

| Username | Password |
|---|---|
| alice | password123 |

## Running tests

```bash
# Unit tests (no server needed)
pytest test_unit.py -v

# Integration tests (requires running server)
uvicorn main:app --port 8000
pytest test_integration.py -v
```