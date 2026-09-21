# WarrantyHub

WarrantyHub is a product warranty registration and claims portal built with a FastAPI backend and a React + Vite frontend. The platform allows customers to register purchases, track warranty status, submit claims, and review product coverage while giving admins tools to manage categories, products, registrations, warranties, and claim decisions.

## Tagline

Track purchases, protect products, and resolve warranty claims faster.

## Overview

This capstone project demonstrates a full-stack workflow where the frontend communicates with a secure REST API, JWT-based authentication is enforced on protected routes, and warranty expiry is calculated in the backend so customers cannot manually override coverage periods.

## Architecture Diagram

```text
React Frontend
  ↓
Render Static Site
  ↓
FastAPI API
  ↓
Render Web Service
  ↓
Railway MySQL
```

## Tech Stack

- Backend: FastAPI, SQLAlchemy, Pydantic, JWT
- Database: MySQL in production; SQLite for local development fallback
- Authentication: bcrypt + passlib + OAuth2 JWT
- Frontend: React, Vite, React Router, Axios, Bootstrap
- Deployment: Render for backend/frontend, Railway for MySQL

## Features

- Customer registration and login
- JWT authentication with protected endpoints
- Role-based admin access control
- Product catalog and category management
- Product registration by customer
- Backend-calculated warranty periods and status values
- Warranty claim submission and admin review workflow
- Swagger/OpenAPI API documentation
- Responsive React dashboard experience

## Screenshots

Add screenshots here once the app is running locally or deployed, for example:

- Login screen
- Customer dashboard
- Product registration page
- Warranty overview
- Admin dashboard

## Local Setup

### 1. Clone and install Python dependencies

```powershell
Set-Location C:\warrentytracker
& .\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 2. Configure environment variables

```powershell
Copy-Item .env.example .env
```

Create a local `.env` file from the example. The project reads `DATABASE_URL`, `SECRET_KEY`, `ALGORITHM`, `ACCESS_TOKEN_EXPIRE_MINUTES`, and `FRONTEND_URL` from the environment. Do not commit `.env` files.

### 3. Run the backend

```powershell
Set-Location C:\warrentytracker
& .\.venv\Scripts\python.exe -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Run the frontend

```powershell
Set-Location C:\warrentytracker\frontend
npm.cmd install
Copy-Item .env.example .env
npm.cmd run dev
```

Then open the local Vite URL, usually `http://localhost:5173`.

### Seed sample products

The existing product model is a catalog model. Run this idempotent command from the repository root to add the demonstration categories and products without changing existing users, registrations, or claims:

```powershell
& .\.venv\Scripts\python.exe -m scripts.seed_products
```

Running it again skips products whose model numbers already exist.

## Environment Variables

Backend variables:

- `DATABASE_URL`
- `SECRET_KEY`
- `ALGORITHM`
- `ACCESS_TOKEN_EXPIRE_MINUTES`
- `FRONTEND_URL`

Frontend variable:

- `VITE_API_URL`

Use `mysql+pymysql://...` for Railway MySQL in production. Keep all real values in the host environment or a local untracked `.env`, never in source control.

## API Documentation

The FastAPI app exposes Swagger UI at:

- `http://localhost:8000/docs`
- `http://localhost:8000/openapi.json`

## Testing Instructions

Run the backend test suite:

```powershell
Set-Location C:\warrentytracker
& .\.venv\Scripts\python.exe -m pytest -q
```

Compile the backend:

```powershell
& .\.venv\Scripts\python.exe -m compileall -q app main.py tests
```

Run the frontend production build:

```powershell
Set-Location C:\warrentytracker\frontend
npm.cmd run build
```

## Deployment Instructions

### Railway MySQL

1. Create a new MySQL database on Railway.
2. Copy the generated database connection string.
3. Save it in the Render backend environment as `DATABASE_URL`.
4. Use the expected format:

```text
mysql+pymysql://USERNAME:PASSWORD@HOST:PORT/DATABASE
```

### Render Backend

1. Create a new Web Service on Render.
2. Set the root directory to the repository root.
3. Use the build command:

```bash
python -m pip install -r requirements.txt
```

4. Use the start command:

```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

5. Add environment variables:

- `DATABASE_URL`
- `SECRET_KEY`
- `ALGORITHM=HS256`
- `ACCESS_TOKEN_EXPIRE_MINUTES=60`
- `FRONTEND_URL`

### Render Frontend

1. Create a new Static Site on Render.
2. Set the root directory to `frontend`.
3. Use the build command:

```bash
npm install && npm run build
```

4. Set the publish directory to `dist`.
5. Add the environment variable:

```text
VITE_API_URL=https://your-render-backend-url
```

6. Ensure the backend `FRONTEND_URL` matches the deployed frontend origin for CORS.

## Folder Structure

```text
warrentytracker/
├── app/
│   ├── api/
│   ├── core/
│   ├── models/
│   ├── schemas/
│   └── services/
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
├── tests/
├── docs/
├── .env.example
├── .gitignore
├── main.py
├── Procfile
├── README.md
├── requirements.txt
└── warrantyhub.db
```

## Future Enhancements

- Invoice and purchase-document uploads
- Email notifications for warranty expiry and claims
- Advanced admin analytics and reports
- Multi-brand inventory support
- Expanded claim scoring and status automation

## License

This project is for educational use and is distributed under the repository license. See `LICENSE` for details.

## Author / Contact

Project author and maintainer details should be added here for the final portfolio submission.

## Deployment Notes

- The backend must not run with a hardcoded port in production.
- The frontend must use `VITE_API_URL` instead of hardcoded API origins.
- CORS should be restricted using the deployed frontend URL in production.
- Do not commit real secret values or MySQL credentials.
