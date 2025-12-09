"""
Authentication endpoints
Handles user registration, login, and token management
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.security import get_current_user, decode_token
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.schemas.token import Token, TokenPair, RefreshToken
from app.services.auth import AuthService

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(
    user_create: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Register a new user

    - **email**: Valid email address
    - **username**: Unique username (3-50 characters)
    - **password**: Strong password (min 8 characters)
    - **full_name**: Optional full name
    """
    auth_service = AuthService(db)
    return auth_service.register(user_create)


@router.post("/login", response_model=TokenPair)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Login with email and password

    Returns access token and refresh token
    """
    auth_service = AuthService(db)
    return auth_service.login(form_data.username, form_data.password)


@router.post("/refresh", response_model=Token)
def refresh_token(
    refresh_data: RefreshToken,
    db: Session = Depends(get_db)
):
    """
    Refresh access token using refresh token
    """
    payload = decode_token(refresh_data.refresh_token)

    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type"
        )

    user_id = payload.get("sub")
    auth_service = AuthService(db)
    return auth_service.refresh_access_token(user_id)


@router.get("/me", response_model=UserResponse)
def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """
    Get current authenticated user information
    """
    return current_user


@router.post("/logout")
def logout(
    current_user: User = Depends(get_current_user)
):
    """
    Logout current user

    Note: For stateless JWT, this is a client-side operation.
    The client should discard the tokens.
    For enhanced security, implement token blacklisting with Redis.
    """
    return {"message": "Successfully logged out", "detail": "Please discard your tokens"}


@router.post("/change-password", response_model=UserResponse)
def change_password(
    current_password: str,
    new_password: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Change current user password
    """
    auth_service = AuthService(db)
    return auth_service.change_password(current_user, current_password, new_password)
