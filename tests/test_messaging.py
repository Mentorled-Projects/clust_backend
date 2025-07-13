import pytest
from fastapi.testclient import TestClient
from main import app
from api.v1.routes.messaging import get_db

@pytest.fixture
def client():
    return TestClient(app)

def test_messaging_list(client, login_data):
    login_response = client.post("/api/v1/auth/login", json=login_data)
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    dummy_group_id = "00000000-0000-0000-0000-000000000000"
    response = client.get(f"/api/v1/message/{dummy_group_id}/messages", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# Additional tests for messaging creation, update, delete, and edge cases to be added here
