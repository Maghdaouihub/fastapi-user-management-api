"""
User management endpoint tests
"""
import pytest
from fastapi import status


def test_get_users_as_superuser(client, superuser_headers, test_user):
    """Test getting all users as superuser"""
    response = client.get("/api/v1/users/", headers=superuser_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2  # At least superuser and test_user


def test_get_users_unauthorized(client):
    """Test getting users without authentication"""
    response = client.get("/api/v1/users/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_users_as_regular_user(client, auth_headers):
    """Test getting users as regular user (should fail)"""
    response = client.get("/api/v1/users/", headers=auth_headers)
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_get_user_by_id(client, auth_headers, test_user):
    """Test getting user by ID (own profile)"""
    response = client.get(f"/api/v1/users/{test_user.id}", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == test_user.id
    assert data["email"] == test_user.email


def test_get_other_user_as_regular_user(client, auth_headers, test_superuser):
    """Test getting other user profile as regular user (should fail)"""
    response = client.get(
        f"/api/v1/users/{test_superuser.id}", headers=auth_headers
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_create_user_as_superuser(client, superuser_headers):
    """Test creating user as superuser"""
    response = client.post(
        "/api/v1/users/",
        headers=superuser_headers,
        json={
            "email": "created@example.com",
            "username": "createduser",
            "password": "password123",
            "full_name": "Created User",
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["email"] == "created@example.com"
    assert data["username"] == "createduser"


def test_update_own_profile(client, auth_headers, test_user):
    """Test updating own profile"""
    response = client.put(
        f"/api/v1/users/{test_user.id}",
        headers=auth_headers,
        json={"full_name": "Updated Name"},
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["full_name"] == "Updated Name"


def test_update_other_user_as_regular_user(client, auth_headers, test_superuser):
    """Test updating other user as regular user (should fail)"""
    response = client.put(
        f"/api/v1/users/{test_superuser.id}",
        headers=auth_headers,
        json={"full_name": "Hacked Name"},
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_delete_user_as_superuser(client, superuser_headers, test_user):
    """Test deleting user as superuser"""
    response = client.delete(
        f"/api/v1/users/{test_user.id}", headers=superuser_headers
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_user_as_regular_user(client, auth_headers, test_superuser):
    """Test deleting user as regular user (should fail)"""
    response = client.delete(
        f"/api/v1/users/{test_superuser.id}", headers=auth_headers
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_activate_user(client, superuser_headers, test_user, db):
    """Test activating a user"""
    # First deactivate
    test_user.is_active = False
    db.commit()

    # Then activate
    response = client.post(
        f"/api/v1/users/{test_user.id}/activate", headers=superuser_headers
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["is_active"] is True


def test_deactivate_user(client, superuser_headers, test_user):
    """Test deactivating a user"""
    response = client.post(
        f"/api/v1/users/{test_user.id}/deactivate", headers=superuser_headers
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["is_active"] is False


def test_get_user_count(client, superuser_headers):
    """Test getting total user count"""
    response = client.get("/api/v1/users/count", headers=superuser_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "count" in data
    assert data["count"] >= 2
