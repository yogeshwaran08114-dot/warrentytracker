# WarrantyHub

A modern warranty management system built with FastAPI and SQLite.

## Features

- User registration with email, mobile, and password
- Secure login with JWT authentication
- Password hashing with bcrypt
- CORS-enabled REST API
- Responsive professional login/signup interface

## Project Structure

```
warrentytracker/
├─ main.py                 # FastAPI entry point
├─ requirements.txt        # Python dependencies
├─ .env.example            # Environment variables
├─ app/
│  ├─ api/                 # Routers/views — thin, no business logic here
│  │  └─ v1/endpoints/
│  │     ├─ auth.py        # Auth endpoints
│  │     └─ users.py       # User endpoints
│  ├─ core/                # Settings, security helpers
│  │  ├─ config.py         # Settings
│  │  ├─ security.py       # Password hashing, JWT
│  │  └─ deps.py           # Database session
│  ├─ models/              # ORM models
│  │  └─ user.py           # SQLAlchemy models
│  ├─ schemas/             # Pydantic schemas
│  │  ├─ user.py           # User schemas
│  │  └─ token.py          # Token schemas
│  └─ services/            # Business logic
│     ├─ user.py           # User CRUD + auth logic
│     └─ auth.py           # Register, login, current user
├─ tests/                  # Unit tests, mirrors app structure
│  ├─ test_api/v1/         # Endpoint tests
│  ├─ test_services/       # Service tests
│  ├─ test_models/         # Model tests
│  └─ test_main.py         # Page/route smoke tests
├─ docs/                   # Diagrams, API contract
│  ├─ architecture.md      # Layered architecture diagram
│  ├─ api-contract.md      # API contract docs
│  └─ api-contract.json    # OpenAPI spec
├─ static/
│  ├─ css/style.css        # Frontend styles
│  └─ js/app.js            # Frontend JavaScript
└─ templates/
   ├─ login.html           # Login page
   ├─ signup.html          # Sign up page
   └─ dashboard.html       # Dashboard page
```

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment:
```bash
cp .env.example .env
```

3. Run the server:
```bash
uvicorn main:app --reload
```

4. Open http://localhost:8000 in your browser.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/v1/auth/register | Register new user |
| POST | /api/v1/auth/login | Login and get JWT token |
| GET | /api/v1/auth/me | Get current user info |
| GET | /api/v1/users | List users |
| GET | /api/v1/users/{id} | Get user by id |

## Running Tests

```bash
pytest
```

## Tech Stack

- **Backend**: FastAPI, SQLAlchemy, Pydantic
- **Database**: SQLite
- **Authentication**: JWT with bcrypt password hashing
- **Frontend**: HTML, CSS, JavaScript (vanilla)
