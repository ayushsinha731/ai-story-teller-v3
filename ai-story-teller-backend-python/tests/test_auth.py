import pytest
from app.schemas.user import User

@pytest.mark.asyncio
async def test_signup(client):
    """Test user registration."""
    response = client.post("/api/user/signup", json={
        "parent_name": "Test Parent",
        "parent_email": "test_signup@example.com",
        "child_name": "Test Child",
        "child_age": 8,
        "password": "Password123!",
        "child_standard": 3
    })
    
    assert response.status_code == 201
    data = response.json()
    assert data["message"] == "User created successfully"
    assert "user" in data
    assert data["user"]["parent_email"] == "test_signup@example.com"
    
    # Verify user in database
    user = await User.find_one(User.parent_email == "test_signup@example.com")
    assert user is not None


@pytest.mark.asyncio
async def test_login(client):
    """Test user login."""
    # First create a user
    signup_data = {
        "parent_name": "Login User",
        "parent_email": "login@example.com",
        "child_name": "Login Child",
        "child_age": 8,
        "password": "Password123!",
        "child_standard": 3
    }
    client.post("/api/user/signup", json=signup_data)
    
    # Now try to login
    response = client.post("/api/user/login", json={
        "email": "login@example.com",
        "password": "Password123!"
    })
    
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "User logged in successfully"
    assert "access_token" in response.cookies or "access_token" in response.headers.get("set-cookie", "")


@pytest.mark.asyncio
async def test_get_me(client, auth_headers):
    """Test getting current user info."""
    # auth_headers fixture already creates a user and logs them in (sets cookies)
    response = client.get("/api/user/me", cookies=auth_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["parent_email"] == "auth_test@example.com"


@pytest.mark.asyncio
async def test_logout(client, auth_headers):
    """Test logout."""
    response = client.post("/api/user/logout", cookies=auth_headers)
    
    assert response.status_code == 200
    assert response.json()["message"] == "Logged out successfully"
    
    # Verify cookie is cleared (FastAPI response should show it)
    # Note: TestClient handles cookies automatically, but checking expired can be tricky
    # We'll just check the response for now
