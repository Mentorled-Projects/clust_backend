import pytest
from fastapi.testclient import TestClient
from main import app
from api.v1.routes.rsvp import get_db

@pytest.fixture
def client():
    return TestClient(app)

def test_rsvp_list(client, login_data):
    login_response = client.post("/api/v1/auth/login", json=login_data)
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/v1/rsvp/my", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# Additional tests for RSVP creation, update, delete, and edge cases to be added here
