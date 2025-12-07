"""
Authentication endpoint tests
"""
import pytest
from fastapi import status


def test_register_user(client, user_data):
    """Test user registration"""
    response = client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["full_name"] == user_data["full_name"]
    assert "id" in data
    assert "hashed_password" not in data


def test_register_duplicate_email(client, user_data):
    """Test registration with duplicate email fails"""
    # Register first user
    client.post("/api/v1/auth/register", json=user_data)

    # Try to register with same email
    response = client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_login_success(client, user_data):
    """Test successful login"""
    # Register user
    client.post("/api/v1/auth/register", json=user_data)

    # Login
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": user_data["email"],
            "password": user_data["password"]
        }
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client, user_data):
    """Test login with wrong password fails"""
    # Register user
    client.post("/api/v1/auth/register", json=user_data)

    # Login with wrong password
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": user_data["email"],
            "password": "WrongPassword"
        }
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_login_nonexistent_user(client):
    """Test login with non-existent user fails"""
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "nonexistent@example.com",
            "password": "SomePassword"
        }
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
