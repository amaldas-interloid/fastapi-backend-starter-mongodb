# FastAPI Backend Starter

A production-ready FastAPI backend starter template built with **FastAPI**, **MongoDB**, **Beanie ODM**, **Redis**, JWT Authentication, RBAC, rate limiting, structured logging, and a Repository-Service architecture.

---

# Features

- FastAPI
- REST API
- API Versioning
- JWT Authentication
- Access & Refresh Tokens
- Token Expiration Handling
- Refresh Token Rotation
- Refresh Token Revocation
- Password Hashing
- User Management
- Role-Based Access Control (RBAC)
- Role Management
- Permission Management
- Permission-Based Authorization
- MongoDB Database
- Beanie ODM
- Repository Pattern
- Service Layer
- Pydantic Validation
- Standard API Response Format
- Pagination
- Filtering
- Sorting
- Soft Delete
- Redis Integration
- Redis Rate Limiting
- CORS Middleware
- Request ID Middleware
- Request Logging Middleware
- Process Time Middleware
- Global Exception Handling
- Structured Logging
- Health Check
- Docker Support
- Docker Compose Support
- Pytest
- Ruff
- MyPy
- Pre-commit

---

# Tech Stack

- Python 3.12+
- FastAPI
- Uvicorn
- MongoDB
- Beanie ODM
- Redis
- Pydantic
- PyJWT
- pwdlib
- Docker
- Docker Compose
- Pytest
- Ruff
- MyPy
- uv

---

# Project Architecture

The project follows a layered architecture using the **Repository-Service pattern**.

```text
app/
├── api/
│   ├── deps.py
│   └── v1/
│       ├── api.py
│       └── endpoints/
│
├── core/
│   ├── config.py
│   ├── logging.py
│   └── security.py
│
├── db/
│   └── database.py
│
├── enums/
│
├── exceptions/
│   ├── exceptions.py
│   └── exception_handlers.py
│
├── middleware/
│   ├── cors.py
│   ├── process_time.py
│   ├── rate_limit.py
│   ├── request_id.py
│   └── request_logging.py
│
├── models/
│
├── repositories/
│
├── schemas/
│
├── services/
│
└── main.py

tests/
├── test_users.py
├── test_rbac.py
├── test_rate_limit.py
├── test_request_id.py
├── test_request_logging.py
└── test_process_time.py

docker/
scripts/
.env
.env.example
Dockerfile
docker-compose.yml
pyproject.toml
uv.lock
README.md

```





# Clone Repository

```bash
git clone git@github.com:amaldas-interloid/fastapi-backend-starter-mongodb.git

cd fastapi-backend-starter-mongodb
```
# Install uv

```bash
pip install uv
```

# Create Virtual Environment

```
uv venv
```
# Activate the virtual environment

source .venv/bin/activate

# Install Dependencies

uv sync

# Configure Environment Variables

Create a `.env` file in the project root.

```env

AAPP_NAME=FastAPI Backend Starter
APP_VERSION=1.0.0

DEBUG=True

HOST=0.0.0.0
PORT=8000

# MongoDB Atlas
MONGODB_URL=your-mongodb-atlas-url
DATABASE_NAME=fastapi_db

JWT_SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

REDIS_RATE_LIMIT=5
REDIS_RATE_LIMIT_WINDOW=60

# Seed
SEED_DEFAULT_PASSWORD=your-default-password
```

---


---

# Seed Database

```bash
uv run python scripts/seed.py
```


---

# Run the Application

```bash
uv run uvicorn app.main:app --reload
```

---

# API Documentation

### Swagger UI

```
http://127.0.0.1:8000/docs
```

### ReDoc

```
http://127.0.0.1:8000/redoc
```

---
