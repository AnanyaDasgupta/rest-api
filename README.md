# Student CRUD REST API

A simple REST API webserver that demonstrates:
- CRUD operations for a `student` resource
- API versioning (`/api/v1/...`)
- Environment-based configuration aligned with Twelve-Factor App principles
- Database schema migrations with Alembic
- Unit tests for endpoints

## Tech Stack
- Python 3.10+
- Flask
- SQLAlchemy
- Alembic
- Pytest

## Features
- `GET /api/v1/healthcheck`
- `POST /api/v1/students`
- `GET /api/v1/students`
- `GET /api/v1/students/<id>`
- `PUT /api/v1/students/<id>`
- `DELETE /api/v1/students/<id>`

## How the app connects to the database
1. `create_app()` loads environment variables (including `.env` in local dev).  
2. `Config.SQLALCHEMY_DATABASE_URI` reads `DATABASE_URL` (falls back to `sqlite:///students.db`).  
3. `db.init_app(app)` initializes Flask-SQLAlchemy with that URI.  
4. API handlers use the shared SQLAlchemy session (`db.session`) for CRUD operations.  
5. Alembic migrations also read `DATABASE_URL` (and `.env`) so schema changes target the same DB.

Examples:
- SQLite (local default): `DATABASE_URL=sqlite:///students.db`
- Postgres: `DATABASE_URL=postgresql+psycopg://user:password@localhost:5432/students`

## Project Setup

### 1) Clone the repository
```bash
git clone <your-public-repo-url>
cd rest-api
```

### 2) Setup environment and dependencies
```bash
make setup
```

### 3) Configure environment variables
Copy `.env.example` to `.env` (or export vars directly in your shell):

```bash
cp .env.example .env
```

Supported env vars:
- `DATABASE_URL` (default: `sqlite:///students.db`)
- `API_VERSION` (default: `v1`)
- `LOG_LEVEL` (default: `INFO`)

### 4) Run migrations
```bash
source .venv/bin/activate
make migrate
```

### 5) Run the API
```bash
source .venv/bin/activate
make run
```

Server runs at: `http://localhost:5000`

## Running Tests
```bash
source .venv/bin/activate
make test
```

## Logging
The app emits logs with levels (`DEBUG`, `INFO`, `WARNING`, etc.) and configurable verbosity using `LOG_LEVEL`.

## API Collection
A Postman collection is included at:
- `postman/student-api.postman_collection.json`

## Twelve-Factor Notes
- Configuration is externalized via environment variables.
- Dependencies are explicitly pinned in `requirements.txt`.
- The app is stateless; persistent state lives in the database.
- Dev/prod parity is improved via repeatable `Makefile` commands.
