import pytest
from unittest.mock import patch, AsyncMock

from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from main import app
from api.v1.routes.auth import get_db

@patch("api.v1.routes.auth.verify_password", return_value=True)
def test_login_success(
    mock_verify_password,
    client,
    verified_user,
    login_data
):
    # Override get_db dependency
    def override_get_db():
        class DummyUser:
            id = 1
            first_name = "Test"
            last_name = "User"
            email = "test.user+unittest@test.com"
            role = "user"
            is_verified = True
            password_hash = "$2b$12$KIXQJ1Q6Q6Q6Q6Q6Q6Q6QO6Q6Q6Q6Q6Q6Q6Q6Q6Q6Q6Q6Q6Q6Q6Q6"  # dummy bcrypt hash

        class DummyResult:
            def scalar_one_or_none(self):
                return DummyUser()

        class DummySession:
            async def execute(self, stmt):
                return DummyResult()

        return DummySession()

    app.dependency_overrides[get_db] = override_get_db

    # Make request
    response = client.post(
        "/api/v1/auth/login",
        json=login_data
    )

    # Debug output
    print("\n=== LOGIN TEST DEBUG ===")
    print("Request data:", login_data)
    print("Response status:", response.status_code)
    print("Response body:", response.json())

    # Assertions
    assert response.status_code == 200, \
        f"Expected 200 OK, got {response.status_code}. Errors: {response.json()}"
    assert "access_token" in response.json()
    assert "token_type" in response.json()

    # Clear dependency override
    app.dependency_overrides = {}

def test_logout_requires_login(client):
    # Make request without auth
    response = client.post("/api/v1/auth/logout")
    
    # Should return 401 Unauthorized
    assert response.status_code == 401

@pytest.mark.asyncio
@patch("api.v1.services.auth.get_user_by_email", new_callable=AsyncMock)
@patch("api.v1.services.auth.create_user", new_callable=AsyncMock)
@patch("api.v1.services.auth.store_token", new_callable=AsyncMock)
@patch("api.utils.email_utils.send_email_reminder", new_callable=AsyncMock)
async def test_signup(
    mock_send_email,
    mock_store_token,
    mock_create_user,
    mock_get_user,
    client,
    user_payload
):
    # Setup mocks
    mock_get_user.return_value = None
    mock_create_user.return_value = AsyncMock(
        id=1,
        email=user_payload["email"],
        is_verified=False
    )
    
    # Make request
    response = client.post("/api/v1/auth/signup", json=user_payload)
    
    # Debug output
    print("\n=== SIGNUP TEST DEBUG ===")
    print("Request payload:", user_payload)
    print("Response status:", response.status_code)
    print("Response body:", response.json())
    
    # Assertions
    assert response.status_code == 200, \
        f"Expected 200 OK, got {response.status_code}. Errors: {response.json()}"
    mock_create_user.assert_called_once()
    mock_store_token.assert_called_once()
    mock_send_email.assert_called_once()

@pytest.mark.asyncio
@patch("api.v1.services.auth.verify_token", new_callable=AsyncMock)
@patch("api.v1.services.auth.get_user_by_email", new_callable=AsyncMock)
@patch("api.v1.services.auth.verify_user_email", new_callable=AsyncMock)
@patch("api.v1.services.auth.delete_token", new_callable=AsyncMock)
async def test_verify_email(
    mock_delete_token,
    mock_verify_user_email,
    mock_get_user,
    mock_verify_token,
    client
):
    # Setup mocks
    test_email = "test.user+unittest@example.com"
    mock_verify_token.return_value = test_email
    mock_get_user.return_value = AsyncMock(email=test_email, is_verified=False)
    
    # Make request
    response = client.post(
        "/api/v1/auth/verify-email",
        json={"token": "valid_token_123"}
    )
    
    # Assertions
    assert response.status_code == 200
    mock_verify_user_email.assert_called_once()
    mock_delete_token.assert_called_once()

@pytest.mark.asyncio
@patch("api.v1.services.auth.get_user_by_email", new_callable=AsyncMock)
@patch("api.utils.email_utils.send_email_reminder", new_callable=AsyncMock)
async def test_resend_verification(
    mock_send_email,
    mock_get_user,
    client
):
    # Setup mocks
    test_email = "test.user+unittest@example.com"
    mock_get_user.return_value = AsyncMock(email=test_email, is_verified=False)
    
    # Make request
    response = client.post(
        "/api/v1/auth/resend-verification",
        json={"email": test_email}
    )
    
    # Assertions
    assert response.status_code == 200
    mock_send_email.assert_called_once()
