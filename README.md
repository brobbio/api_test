# Items App

A simple full-stack application for storing and retrieving items. The project consists of a FastAPI backend, a PostgreSQL database, and a Vue.js frontend served as static files.

## Features

- JWT-based authentication
- Role-based authorization (RBAC)
- Item creation and retrieval
- Paginated item listing
- PostgreSQL persistence
- Automatic database schema creation
- Automatic seeding of default users
- Dockerized deployment with Docker Compose
- Backend endpoint tests with pytest

## Authorization Model

The application defines two user roles:

| Role | Permissions |
|--------|-------------|
| maintainer | Create and view items |
| clerk | View items only |

Authorization is enforced at the API layer using FastAPI dependencies.

## Technology Stack

### Backend

- FastAPI
- SQLAlchemy
- PostgreSQL
- JWT Authentication
- Pytest

### Frontend

- Vue 3 (CDN, no build step)
- HTML/CSS/JavaScript

### Infrastructure

- Docker
- Docker Compose

## Project Structure

```text
.
├── src/
│   ├── main.py
│   ├── models/
│   ├── routers/
│   ├── schema/
│   ├── services/
│   ├── dependencies.py
│   └── db.py
├── frontend/
│   ├── index.html
│   ├── app.js
│   ├── style.css
│   ├── login.html
│   └── login.js
├── tests/
│   └── test_items.py
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
├── entrypoint.sh
└── README.md
```

## Running the Application

Start the complete stack:

```bash
docker compose up --build
```

This launches:

- FastAPI backend
- PostgreSQL database
- Frontend static assets

## Database Initialization

On startup, the application:

1. Creates all required database tables.
2. Seeds default users if they do not already exist.

To recreate the database from scratch:

```bash
docker compose down -v
docker compose up --build
```

## Default Users

The application automatically creates the following users:

| Username | Password | Role |
|----------|----------|------|
| user_maintainer | maintainer_password | maintainer |
| user_clerk | clerk_password | clerk |

> The maintainer user can create and view items. The clerk user can only view items.

## Accessing the Application

| Service | URL |
|----------|-----|
| Frontend | http://localhost:8080 |
| Backend API | http://localhost:8000 |
| Swagger UI | http://localhost:8000/docs |

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|----------|----------|-------------|
| POST | `/auth/login` | Authenticate and receive a JWT |
| DELETE | `/auth/logout` | Logout and invalidate the current token |

### Items

| Method | Endpoint | Authorization | Description |
|----------|----------|---------------|-------------|
| GET | `/items` | clerk, maintainer | Retrieve a paginated list of items |
| GET | `/items/{id}` | clerk, maintainer | Retrieve a single item |
| POST | `/items` | maintainer only | Create a new item |

## Pagination

The item list endpoint supports pagination through query parameters:

```http
GET /items?limit=10&offset=0
```

Example:

```http
GET /items?limit=10&offset=20
```

Returns items 21–30.

## Running Tests

Run backend tests from the project root:

```bash
pytest
```

The test suite covers:

- Authentication
- Authorization
- Item creation
- Item retrieval
- API response validation

## Example Workflow

### Maintainer Workflow

1. Log in as `user_maintainer`.
2. Create one or more items.
3. View items from the frontend.
4. Navigate paginated results using the Previous and Next controls.
5. Explore the API through Swagger UI at `/docs`.

### Clerk Workflow

1. Log in as `user_clerk`.
2. View existing items.
3. Attempting to create an item will result in a `403 Forbidden` response due to insufficient permissions.

## Security Notes

- Passwords are stored as hashes.
- Authentication is handled using JWT tokens.
- Protected endpoints require a valid Bearer token.
- Authorization is enforced using role-based permissions.