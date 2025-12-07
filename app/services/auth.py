"""
Authentication service - Business logic for auth operations
"""
from typing import Optional
from datetime import timedelta
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import verify_password, create_access_token, create_refresh_token, decode_token
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate
from app.schemas.token import TokenResponse
from app.services.user import UserService


class AuthService:
    """
    Authentication service with business logic
    """

    def __init__(self, db: Session):
        self.db = db
        self.user_repository = UserRepository(db)
        self.user_service = UserService(db)

    def register(self, user_in: UserCreate) -> Optional[User]:
        """
        Register a new user

        Args:
            user_in: User registration data

        Returns:
            Created user or None if email exists
        """
        return self.user_service.create(user_in)

    def login(self, email: str, password: str) -> Optional[TokenResponse]:
        """
        Authenticate user and generate tokens

        Args:
            email: User email
            password: User password

        Returns:
            Token response or None if authentication fails
        """
        # Get user by email
        user = self.user_repository.get_by_email(email)

        if user is None:
            return None

        # Verify password
        if not verify_password(password, user.hashed_password):
            return None

        # Check if user is active
        if not user.is_active:
            return None

        # Generate tokens
        access_token = create_access_token(
            data={"sub": user.id},
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )

        refresh_token = create_refresh_token(
            data={"sub": user.id},
            expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        )

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )

    def refresh_token(self, refresh_token: str) -> Optional[TokenResponse]:
        """
        Refresh access token using refresh token

        Args:
            refresh_token: Valid refresh token

        Returns:
            New token response or None if invalid
        """
        # Decode refresh token
        payload = decode_token(refresh_token)

        if payload is None:
            return None

        # Validate token type
        if payload.get("type") != "refresh":
            return None

        # Get user ID
        user_id = payload.get("sub")
        if user_id is None:
            return None

        # Get user
        user = self.user_repository.get(user_id)

        if user is None or not user.is_active:
            return None

        # Generate new tokens
        access_token = create_access_token(
            data={"sub": user.id},
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )

        new_refresh_token = create_refresh_token(
            data={"sub": user.id},
            expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        )

        return TokenResponse(
            access_token=access_token,
            refresh_token=new_refresh_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
