
# FastAPI Backend Starter

A production-ready FastAPI starter template with a scalable project structure and modern development tools.

## Features

- FastAPI
- uv package manager
- Environment-based configuration
- Modular project structure
- SQLAlchemy (planned)
- Alembic migrations (planned)
- PostgreSQL (planned)
- Redis (planned)
- JWT Authentication (planned)
- Docker support (planned)
- Pytest (planned)
- GitHub Actions (planned)

## Project Structure

```text
.
├── app
│   ├── api
│   ├── core
│   ├── db
│   ├── middleware
│   ├── models
│   ├── repositories
│   ├── schemas
│   ├── services
│   ├── utils
│   └── main.py
├── migrations
├── tests
├── docker
├── scripts
├── pyproject.toml
├── uv.lock
└── README.md
```

## Getting Started

```bash
uv sync
uv run uvicorn app.main:app --reload
```

API Documentation:

- http://127.0.0.1:8000/docs
- http://127.0.0.1:8000/redoc

## Development Workflow

- main → Production
- develop → Integration
- feature/* → Feature development

## Configuration

The project uses **pydantic-settings** to manage configuration.

Create your local environment file:

```bash
cp .env.example .env
```

Application settings are loaded automatically from `.env`.

## API Structure

The project organizes endpoints by API version.

```text
app/api/
├── deps.py
└── v1/
    ├── api.py
    └── endpoints/
```

All routers are registered in `app/api/v1/api.py` and included in `app/main.py`.
## Logging

The application uses Python's built-in `logging` module with centralized configuration.

### Features

- Centralized logging configuration
- Configurable log level
- Startup and shutdown logging
- Standardized log format

## Middleware

### CORS

The application enables CORS middleware to allow frontend applications to communicate with the API.

**Development**

- All origins are allowed (`*`).

**Production**

- Replace `allow_origins=["*"]` with a list of trusted frontend domains.

### Request Logging

Logs every HTTP request with:

- HTTP method
- Request path
- Response status code

### Base Models

The project uses reusable SQLAlchemy mixins to provide:

- UUID primary keys
- Automatic `created_at` timestamps
- Automatic `updated_at` timestamps