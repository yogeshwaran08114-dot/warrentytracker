def test_health_endpoint(client):
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json() == {
        "success": True,
        "data": {"status": "healthy"},
        "message": "Service is healthy",
    }


def test_backend_does_not_serve_frontend_pages(client):
    response = client.get("/login.html")

    assert response.status_code == 404
