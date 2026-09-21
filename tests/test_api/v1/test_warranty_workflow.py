from app.models.user import User


def register(client, email):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "password": "password123",
            "confirm_password": "password123",
            "full_name": "Test User",
        },
    )
    assert response.status_code == 201
    return response.json()


def token(client, email):
    response = client.post(
        "/api/v1/auth/login",
        data={"username": email, "password": "password123"},
    )
    assert response.status_code == 200
    return response.json()["access_token"]


def test_customer_warranty_claim_and_admin_workflow(client, db_session):
    admin_email = "workflow-admin@example.com"
    customer_email = "workflow-customer@example.com"
    register(client, admin_email)
    admin = db_session.query(User).filter(User.email == admin_email).one()
    admin.role = "admin"
    db_session.commit()

    admin_headers = {"Authorization": f"Bearer {token(client, admin_email)}"}
    register(client, customer_email)
    customer_headers = {"Authorization": f"Bearer {token(client, customer_email)}"}

    assert client.get("/api/v1/admin/registrations", headers=customer_headers).status_code == 403
    category = client.post(
        "/api/v1/categories",
        headers=admin_headers,
        json={"name": "Laptops", "description": "Portable computers"},
    )
    assert category.status_code == 201
    product = client.post(
        "/api/v1/products",
        headers=admin_headers,
        json={
            "product_name": "Example Laptop",
            "brand": "Example",
            "model_number": "EX-1",
            "category_id": category.json()["data"]["id"],
            "default_warranty_months": 1,
        },
    )
    assert product.status_code == 201

    registration = client.post(
        "/api/v1/registrations",
        headers=customer_headers,
        json={
            "product_id": product.json()["data"]["id"],
            "serial_number": "SERIAL-001",
            "purchase_date": "2024-01-31",
        },
    )
    assert registration.status_code == 201
    registration_data = registration.json()["data"]
    assert registration_data["warranty_expiry_date"] == "2024-02-29"

    claim = client.post(
        "/api/v1/claims",
        headers=customer_headers,
        json={
            "registration_id": registration_data["id"],
            "issue_description": "The screen does not turn on.",
        },
    )
    assert claim.status_code == 201
    claim_id = claim.json()["data"]["id"]
    claims = client.get("/api/v1/admin/claims", headers=admin_headers)
    assert claims.status_code == 200
    assert claims.json()["data"][0]["id"] == claim_id

    update = client.put(
        f"/api/v1/admin/claims/{claim_id}",
        headers=admin_headers,
        json={"status": "Approved", "admin_remarks": "Reviewed by support."},
    )
    assert update.status_code == 200
    assert update.json()["data"]["status"] == "Approved"