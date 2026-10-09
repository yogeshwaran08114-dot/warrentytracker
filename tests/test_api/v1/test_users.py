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

def admin_headers(client, db_session):
    register_user(client, email="admin@example.com")
    from app.models.user import User

    admin = db_session.query(User).filter(User.email == "admin@example.com").one()
    admin.role = "admin"
    db_session.commit()
    token = client.post(
        "/api/v1/auth/login",
        data={"username": "admin@example.com", "password": "password123"},
    ).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_list_users_returns_registered_users(client, db_session):
    register_user(client)
    register_user(client, email="bob@example.com")
    resp = client.get("/api/v1/users", headers=admin_headers(client, db_session))
    assert resp.status_code == 200
    assert len(resp.json()) == 3


def test_get_user_by_id(client, db_session):
    user = register_user(client).json()
    resp = client.get(f"/api/v1/users/{user['id']}", headers=admin_headers(client, db_session))
    assert resp.status_code == 200
    assert resp.json()["email"] == "alice@example.com"


def test_get_user_not_found_returns_404(client, db_session):
    resp = client.get("/api/v1/users/999", headers=admin_headers(client, db_session))
    assert resp.status_code == 404

def test_list_users_without_admin_token_returns_403(client):
    register_user(client)
    token = client.post(
        "/api/v1/auth/login",
        data={"username": "alice@example.com", "password": "password123"},
    ).json()["access_token"]

    resp = client.get(
        "/api/v1/users",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert resp.status_code == 403