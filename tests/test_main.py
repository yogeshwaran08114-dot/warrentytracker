def test_root_redirects_to_login(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.url.path == "/login.html"


def test_login_page_renders(client):
    resp = client.get("/login.html")
    assert resp.status_code == 200
    assert "login" in resp.text.lower()


def test_signup_page_renders(client):
    resp = client.get("/signup.html")
    assert resp.status_code == 200
    assert "signup" in resp.text.lower() or "register" in resp.text.lower()


def test_dashboard_page_renders(client):
    resp = client.get("/dashboard.html")
    assert resp.status_code == 200
    assert "dashboard" in resp.text.lower()
