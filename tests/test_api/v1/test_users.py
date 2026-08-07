def register_user(client, email="alice@example.com"):
    return client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "password": "password123",
            "confirm_password": "password123",
            "full_name": "Alice",
        },
    )


def test_list_users_returns_registered_users(client):
    register_user(client)
    register_user(client, email="bob@example.com")
    resp = client.get("/api/v1/users")
    assert resp.status_code == 200
    assert len(resp.json()) == 2


def test_get_user_by_id(client):
    user = register_user(client).json()
    resp = client.get(f"/api/v1/users/{user['id']}")
    assert resp.status_code == 200
    assert resp.json()["email"] == "alice@example.com"


def test_get_user_not_found_returns_404(client):
    resp = client.get("/api/v1/users/999")
    assert resp.status_code == 404
