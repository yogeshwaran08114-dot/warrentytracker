def register_user(client, email="alice@example.com", password="password123"):
    return client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "password": password,
            "confirm_password": password,
            "full_name": "Alice",
            "mobile_number": "1234567890",
        },
    )


def test_register_endpoint_creates_user(client):
    resp = register_user(client)
    assert resp.status_code == 201
    body = resp.json()
    assert body["email"] == "alice@example.com"
    assert "hashed_password" not in body


def test_register_duplicate_email_returns_400(client):
    register_user(client)
    resp = register_user(client)
    assert resp.status_code == 400


def test_register_short_password_returns_422(client):
    resp = client.post(
        "/api/v1/auth/register",
        json={
            "email": "bob@example.com",
            "password": "short",
            "confirm_password": "short",
        },
    )
    assert resp.status_code == 422


def test_login_endpoint_returns_token(client):
    register_user(client)
    resp = client.post(
        "/api/v1/auth/login",
        data={"username": "alice@example.com", "password": "password123"},
    )
    assert resp.status_code == 200
    assert resp.json()["token_type"] == "bearer"
    assert "access_token" in resp.json()


def test_login_wrong_password_returns_401(client):
    register_user(client)
    resp = client.post(
        "/api/v1/auth/login",
        data={"username": "alice@example.com", "password": "wrongpass"},
    )
    assert resp.status_code == 401


def test_me_endpoint_returns_current_user(client):
    register_user(client)
    token_resp = client.post(
        "/api/v1/auth/login",
        data={"username": "alice@example.com", "password": "password123"},
    )
    token = token_resp.json()["access_token"]
    resp = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    assert resp.json()["email"] == "alice@example.com"


def test_me_endpoint_invalid_token_returns_401(client):
    resp = client.get("/api/v1/auth/me", headers={"Authorization": "Bearer bogus"})
    assert resp.status_code == 401

def test_login_unknown_email_returns_401(client):
    resp = client.post(
        "/api/v1/auth/login",
        data={"username": "unknown@example.com", "password": "password123"},
    )
    assert resp.status_code == 401

def test_register_mismatched_passwords_returns_422(client):
    resp = client.post(
        "/api/v1/auth/register",
        json={
            "email": "mismatch@example.com",
            "password": "password123",
            "confirm_password": "different123",
            "full_name": "Mismatch User",
            "mobile_number": "1234567890",
        },
    )
    assert resp.status_code == 422