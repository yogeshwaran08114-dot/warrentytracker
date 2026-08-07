# Architecture

WarrantyHub follows a **layered architecture**: thin API routers delegate to
services, which own the business logic and talk to the ORM models through a
database session. Schemas define the API contract at the edges.

```mermaid
flowchart TD
    subgraph Client
        UI[Browser / SPA]
    end

    subgraph App["app/ (FastAPI)"]
        direction TB
        API["api/ (routers)<br/>thin HTTP layer, no business logic"]
        CORE["core/<br/>config, security, db deps"]
        SERVICES["services/ (business logic)"]
        MODELS["models/ (SQLAlchemy ORM)"]
        SCHEMAS["schemas/ (Pydantic)"]
    end

    DB[(SQLite<br/>warrantyhub.db)]

    UI -->|HTTP /api/v1| API
    API -->|Pydantic validation| SCHEMAS
    API --> SERVICES
    SERVICES -->|password hash / JWT| CORE
    SERVICES --> MODELS
    CORE -->|engine / session| DB
    MODELS -->|queries| DB
    SERVICES --> SCHEMAS
```

## Request flow

1. A request hits a router in `app/api/v1/endpoints/` (e.g. `POST /api/v1/auth/login`).
2. FastAPI validates the payload against a Pydantic schema (`app/schemas/`).
3. The router calls a function in `app/services/` — no business logic lives in the router.
4. The service uses `app/core/` helpers (password hashing, JWT, config) and reads/writes rows through `app/models/`.
5. The service returns data, which FastAPI serializes back through the schema.

## Test flow

`tests/` mirrors `app/`:

- `tests/test_api/v1/` — endpoint tests through `TestClient`
- `tests/test_services/` — service unit tests against an in-memory SQLite database
- `tests/test_models/` — ORM model schema tests
- `tests/test_main.py` — page/route smoke tests
