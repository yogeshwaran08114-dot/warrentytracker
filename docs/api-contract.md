# API Contract

Base URL: `http://localhost:8000/api/v1`

The machine-readable contract is in [`api-contract.json`](api-contract.json)
(OpenAPI 3.1). Interactive docs are served at `/docs` when the app is running.

## Endpoints

### Auth

| Method | Path             | Auth | Description                |
|--------|------------------|------|----------------------------|
| POST   | `/auth/register` | No   | Create a new user account  |
| POST   | `/auth/login`    | No   | Authenticate, get a JWT    |
| GET    | `/auth/me`       | Bearer | Get the current user     |

### Users

| Method | Path            | Auth | Description                    |
|--------|-----------------|------|--------------------------------|
| GET    | `/users`        | No   | List users (`skip`, `limit`)   |
| GET    | `/users/{id}`   | No   | Get a single user by id        |

## Examples

### Register a user

```http
POST /api/v1/auth/register
Content-Type: application/json

{
  "email": "alice@example.com",
  "password": "password123",
  "confirm_password": "password123",
  "full_name": "Alice",
  "mobile_number": "1234567890"
}
```

**201 Created**

```json
{
  "email": "alice@example.com",
  "full_name": "Alice",
  "mobile_number": "1234567890",
  "id": 1,
  "is_active": true,
  "created_at": "2026-08-07T12:00:00"
}
```

### Login

```http
POST /api/v1/auth/login
Content-Type: application/x-www-form-urlencoded

username=alice%40example.com&password=password123
```

**200 OK**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

### Get current user

```http
GET /api/v1/auth/me
Authorization: Bearer <access_token>
```

**200 OK**

```json
{
  "email": "alice@example.com",
  "full_name": "Alice",
  "mobile_number": "1234567890",
  "id": 1,
  "is_active": true,
  "created_at": "2026-08-07T12:00:00"
}
```

## Error responses

| Status | Body                                          | When                          |
|--------|-----------------------------------------------|-------------------------------|
| 400    | `{"detail": "Email already registered"}`      | Duplicate email               |
| 401    | `{"detail": "Incorrect email or password"}`   | Bad credentials / bad token   |
| 404    | `{"detail": "User not found"}`                | Unknown user id               |
| 422    | `{"detail": "Validation error", "errors": [...]}` | Invalid request payload   |

## Authentication

Login returns a JWT (`HS256`). Send it as `Authorization: Bearer <token>`.
Tokens expire after `ACCESS_TOKEN_EXPIRE_MINUTES` (default 30).
