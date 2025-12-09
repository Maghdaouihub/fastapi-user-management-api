"""
User management endpoints
CRUD operations for users (admin only)
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.core.security import get_current_user, get_current_superuser
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.services.user import UserService

router = APIRouter()


@router.get("/me", response_model=UserResponse)
def get_current_user_profile(
    current_user: User = Depends(get_current_user)
):
    """
    Get current authenticated user profile
    """
    return current_user


@router.put("/me", response_model=UserResponse)
def update_current_user_profile(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update current authenticated user profile
    """
    user_service = UserService(db)
    return user_service.update_user(current_user.id, user_update)


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_current_user_account(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete current authenticated user account
    """
    user_service = UserService(db)
    user_service.delete_user(current_user.id)
    return None


@router.get("/", response_model=List[UserResponse])
def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
):
    """
    Get list of all users (admin only)

    - **skip**: Number of records to skip (pagination)
    - **limit**: Maximum number of records to return
    """
    user_service = UserService(db)
    return user_service.get_users(skip=skip, limit=limit)


@router.get("/active", response_model=List[UserResponse])
def get_active_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
):
    """
    Get list of active users (admin only)
    """
    user_service = UserService(db)
    return user_service.get_active_users(skip=skip, limit=limit)


@router.get("/count")
def get_user_count(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
):
    """
    Get total user count (admin only)
    """
    user_service = UserService(db)
    return {"count": user_service.get_user_count()}


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get user by ID

    Users can only view their own profile unless they're admin
    """
    if not current_user.is_superuser and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough privileges"
        )

    user_service = UserService(db)
    return user_service.get_user(user_id)


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user_create: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
):
    """
    Create a new user (admin only)
    """
    user_service = UserService(db)
    return user_service.create_user(user_create)


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update user information

    Users can only update their own profile unless they're admin
    """
    if not current_user.is_superuser and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough privileges"
        )

    user_service = UserService(db)
    return user_service.update_user(user_id, user_update)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
):
    """
    Delete a user (admin only)
    """
    user_service = UserService(db)
    user_service.delete_user(user_id)
    return None


@router.post("/{user_id}/activate", response_model=UserResponse)
def activate_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
):
    """
    Activate a user (admin only)
    """
    user_service = UserService(db)
    return user_service.activate_user(user_id)


@router.post("/{user_id}/deactivate", response_model=UserResponse)
def deactivate_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
):
    """
    Deactivate a user (admin only)
    """
    user_service = UserService(db)
    return user_service.deactivate_user(user_id)
