from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_healthcheck():
    response = client.get("/healthcheck")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_cors_headers():
    response = client.options("/healthcheck", headers={
        "Origin": "http://example.com",
        "Access-Control-Request-Method": "GET"
    })
    assert response.status_code == 200
    assert "access-control-allow-origin" in response.headers
    assert response.headers["access-control-allow-origin"] == "http://example.com" or response.headers["access-control-allow-origin"] == "*"

def test_included_routes():
    response = client.post("/api/v1/user/signup", json={
        "email": "testmain@example.com",
        "password": "password123"
    })
    assert response.status_code in [200, 400]
