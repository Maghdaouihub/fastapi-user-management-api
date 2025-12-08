"""
User service
Handles user management business logic
"""
from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserUpdate


class UserService:
    """User service with business logic"""

    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)

    def get_user(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        user = self.user_repo.get(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return user

    def get_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get list of users with pagination"""
        return self.user_repo.get_multi(skip=skip, limit=limit)

    def get_active_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get list of active users"""
        return self.user_repo.get_active_users(skip=skip, limit=limit)

    def create_user(self, user_create: UserCreate) -> User:
        """Create a new user"""
        # Check if email exists
        existing_user = self.user_repo.get_by_email(user_create.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        # Check if username exists
        existing_username = self.user_repo.get_by_username(user_create.username)
        if existing_username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken",
            )

        # Create user
        hashed_password = get_password_hash(user_create.password)
        user_data = {
            "email": user_create.email,
            "username": user_create.username,
            "full_name": user_create.full_name,
            "hashed_password": hashed_password,
        }

        return self.user_repo.create(user_data)

    def update_user(self, user_id: int, user_update: UserUpdate) -> User:
        """Update user information"""
        user = self.user_repo.get(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        # Prepare update data
        update_data = user_update.dict(exclude_unset=True)

        # Hash password if provided
        if "password" in update_data:
            update_data["hashed_password"] = get_password_hash(
                update_data.pop("password")
            )

        # Check email uniqueness if changing
        if "email" in update_data and update_data["email"] != user.email:
            existing_user = self.user_repo.get_by_email(update_data["email"])
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered",
                )

        return self.user_repo.update(user_id, update_data)

    def delete_user(self, user_id: int) -> bool:
        """Delete a user"""
        user = self.user_repo.get(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        return self.user_repo.delete(user_id)

    def activate_user(self, user_id: int) -> User:
        """Activate a user"""
        return self.user_repo.update(user_id, {"is_active": True})

    def deactivate_user(self, user_id: int) -> User:
        """Deactivate a user"""
        return self.user_repo.update(user_id, {"is_active": False})

    def get_user_count(self) -> int:
        """Get total user count"""
        return self.user_repo.count()
