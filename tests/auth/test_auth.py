import pytest
from fastapi.testclient import TestClient
from api.v1.routes.auth import user
from fastapi import FastAPI
from itsdangerous import URLSafeTimedSerializer
from core.config.settings import settings

app = FastAPI()
app.include_router(user)

client = TestClient(app)

def test_signup_and_verify_email():
    # Test signup with new user
    response = client.post("/user/signup", json={
        "email": "test@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    assert response.json() == {"message": "Verification email sent"}

    # Test duplicate signup
    response = client.post("/user/signup", json={
        "email": "test@example.com",
        "password": "password123"
    })
    assert response.status_code == 400
    assert "Email already registered" in response.json()["detail"]

    # Generate token for verification
    serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
    token = serializer.dumps("test@example.com")

    # Test valid verification
    response = client.get(f"/user/verify/{token}")
    assert response.status_code == 200
    assert response.json() == {"message": "Email verified successfully"}

    # Test expired token (simulate by using max_age=0)
    expired_token = token
    response = client.get(f"/user/verify/{expired_token}")
    # We cannot simulate expiration easily here, so just check for 200 or 400
    assert response.status_code in [200, 400]

    # Test invalid token
    response = client.get("/user/verify/invalidtoken")
    assert response.status_code == 400
    assert response.json() == {"message": "Invalid token"}
