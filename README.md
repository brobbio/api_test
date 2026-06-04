<<<<<<< Updated upstream
=======
# Items App

A simple full-stack application for storing and retrieving items. The project consists of a FastAPI backend, a PostgreSQL database, and a Vue.js frontend served as static files.

## Features

* JWT-based authentication
* Item creation and retrieval
* Paginated item listing
* PostgreSQL persistence
* Dockerized deployment with Docker Compose
* Automated database schema initialization
* Backend endpoint tests with pytest

## Technology Stack

### Backend

* FastAPI
* SQLAlchemy
* PostgreSQL
* JWT Authentication

### Frontend

* Vue 3 (CDN, no build step)
* HTML/CSS/JavaScript

### Infrastructure

* Docker
* Docker Compose

## Project Structure

```text
.
├── src/
│   ├── main.py
│   ├── models.py
│   ├── routes.py
│   └── db.py
├── sql/
│   └── schema.sql
├── frontend/
│   ├── index.html
│   ├── app.js
│   ├── style.css
│   ├── login.html
│   └── login.js
├── tests/
│   └── endpoint_tests.py
├── docker-compose.yml
├── Dockerfile
├── setup.py
├── entrypoint.sh
└── README.md
```

## Running the Application

Start the entire stack:

```bash
docker compose up --build
```

This will start:

* FastAPI backend
* PostgreSQL database
* Frontend assets

## Database Initialization

The PostgreSQL container automatically initializes the database schema from:

```text
sql/schema.sql
```

during first startup.

If you need to recreate the database from scratch:

```bash
docker compose down -v
docker compose up --build
```

## Accessing the Application

| Service     | URL                        |
| ----------- | -------------------------- |
| Frontend    | http://localhost:8080      |
| Backend API | http://localhost:8000      |
| Swagger UI  | http://localhost:8000/docs |

## API Endpoints

### Authentication

| Method | Endpoint       | Description                             |
| ------ | -------------- | --------------------------------------- |
| POST   | `/auth/login`  | Authenticate and receive a JWT          |
| DELETE | `/auth/logout` | Logout and invalidate the current token |

### Items

| Method | Endpoint      | Description                        |
| ------ | ------------- | ---------------------------------- |
| GET    | `/items`      | Retrieve a paginated list of items |
| GET    | `/items/{id}` | Retrieve a single item by ID       |
| POST   | `/items`      | Create a new item                  |

### Pagination

The list endpoint supports pagination via query parameters:

```http
GET /items?limit=10&offset=0
```

Example:

```http
GET /items?limit=10&offset=20
```

returns items 21–30.

## Test User

| Username | Password |
| -------- | -------- |
| user     | password |

## Running Tests

Run the backend tests from the application container:

```bash
docker exec -it items-app pytest tests/endpoint_tests.py -v
```

## Example Workflow

1. Log in using the test credentials.
2. Create one or more items.
3. View stored items in the frontend.
4. Navigate through paginated results using the Previous and Next controls.
5. Inspect the API using Swagger at `/docs`.

```
>>>>>>> Stashed changes
