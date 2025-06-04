import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock
from main import app
from httpx import AsyncClient
import pytest_asyncio

@pytest.fixture
def client():
    return TestClient(app)

@pytest_asyncio.fixture
async def async_client():
    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        yield ac

@pytest.fixture
def user_payload():
    return {
        "email": "test.user+unittest@test.com",
        "first_name": "Test",
        "last_name": "User",
        "password": "SecurePass123!",
        "password_verify": "SecurePass123!",
        "accept_terms": True,
        "username": "testuser"  # Add if required by your model
    }

@pytest.fixture
def login_data():
    return {
        "email": "test.user+unittest@test.com",
        "password": "SecurePass123!"
    }

@pytest.fixture
def verified_user():
    return AsyncMock(
        id=1,
        email="test.user+unittest@example.com",
        first_name="Test",
        last_name="User",
        password_hash="hashed_password",
        is_verified=True,
        role="user"
    )
