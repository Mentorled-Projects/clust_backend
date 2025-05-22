import pytest
from httpx import AsyncClient
from main import app

@pytest.mark.asyncio
async def test_me_and_logout_endpoints():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Login to get token
        login_response = await ac.post("/api/v1/user/login", json={
            "email": "testuser@example.com",
            "password": "TestPassword1!"
        })
        assert login_response.status_code == 200
        token = login_response.json().get("access_token")
        assert token is not None

        headers = {"Authorization": f"Bearer {token}"}

        # Call /me endpoint with token
        me_response = await ac.get("/api/v1/user/me", headers=headers)
        assert me_response.status_code == 200
        user_data = me_response.json()
        assert user_data.get("email") == "testuser@example.com"

        # Call /logout endpoint with token
        logout_response = await ac.post("/api/v1/user/logout", headers=headers)
        assert logout_response.status_code == 200
        assert logout_response.json().get("detail") == "Logged out successfully"

        # Call /me endpoint again with the same token, expect 401
        me_response_after_logout = await ac.get("/api/v1/user/me", headers=headers)
        assert me_response_after_logout.status_code == 401
        assert me_response_after_logout.json().get("detail") == "Token has been revoked"
