"""
Authentication service
Handles user registration, login, and token management
"""
from datetime import timedelta
from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import (
    create_access_token,
    create_refresh_token,
    get_password_hash,
    verify_password,
)
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate
from app.schemas.token import Token, TokenPair


class AuthService:
    """Authentication service with business logic"""

    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)

    def register(self, user_create: UserCreate) -> User:
        """Register a new user"""
        # Check if user already exists
        existing_user = self.user_repo.get_by_email(user_create.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        # Check if username is taken
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
            "is_active": True,
            "is_superuser": False,
        }

        return self.user_repo.create(user_data)

    def login(self, email: str, password: str) -> TokenPair:
        """Login and return access and refresh tokens"""
        user = self.user_repo.authenticate(email, password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Inactive user",
            )

        # Create tokens
        access_token = create_access_token(data={"sub": user.id})
        refresh_token = create_refresh_token(data={"sub": user.id})

        return TokenPair(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
        )

    def refresh_access_token(self, user_id: int) -> Token:
        """Create new access token from refresh token"""
        user = self.user_repo.get(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Inactive user",
            )

        access_token = create_access_token(data={"sub": user.id})
        return Token(access_token=access_token, token_type="bearer")

    def change_password(
        self, user: User, current_password: str, new_password: str
    ) -> User:
        """Change user password"""
        if not verify_password(current_password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect password",
            )

        hashed_password = get_password_hash(new_password)
        return self.user_repo.update(
            user.id, {"hashed_password": hashed_password}
        )
