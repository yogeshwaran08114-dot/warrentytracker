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
│  ├─ core/
│  │  ├─ config.py         # Settings
│  │  ├─ security.py       # Password hashing, JWT
│  │  └─ deps.py           # Database session
│  ├─ models/
│  │  └─ user.py           # SQLAlchemy models
│  ├─ schemas/
│  │  ├─ user.py           # Pydantic schemas
│  │  └─ token.py          # Token schemas
│  ├─ crud/
│  │  └─ user.py           # Database operations
│  └─ api/v1/endpoints/
│     ├─ auth.py           # Auth endpoints
│     └─ users.py          # User endpoints
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

## Tech Stack

- **Backend**: FastAPI, SQLAlchemy, Pydantic
- **Database**: SQLite
- **Authentication**: JWT with bcrypt password hashing
- **Frontend**: HTML, CSS, JavaScript (vanilla)
