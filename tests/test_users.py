"""
User endpoint tests
"""
import pytest
from fastapi import status


def get_auth_headers(client, user_data):
    """Helper to get authentication headers"""
    # Register and login
    client.post("/api/v1/auth/register", json=user_data)
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": user_data["email"],
            "password": user_data["password"]
        }
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_get_current_user(client, user_data):
    """Test getting current user profile"""
    headers = get_auth_headers(client, user_data)

    response = client.get("/api/v1/users/me", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["full_name"] == user_data["full_name"]


def test_get_current_user_unauthorized(client):
    """Test getting current user without authentication fails"""
    response = client.get("/api/v1/users/me")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_update_current_user(client, user_data):
    """Test updating current user"""
    headers = get_auth_headers(client, user_data)

    update_data = {"full_name": "Updated Name"}
    response = client.put("/api/v1/users/me", json=update_data, headers=headers)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["full_name"] == "Updated Name"


def test_delete_current_user(client, user_data):
    """Test deleting current user"""
    headers = get_auth_headers(client, user_data)

    response = client.delete("/api/v1/users/me", headers=headers)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Try to get user profile after deletion
    response = client.get("/api/v1/users/me", headers=headers)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
