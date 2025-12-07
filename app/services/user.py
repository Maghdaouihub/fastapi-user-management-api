"""
User service - Business logic for user operations
"""
from typing import Optional, List
from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserUpdate


class UserService:
    """
    User service with business logic
    """

    def __init__(self, db: Session):
        self.db = db
        self.repository = UserRepository(db)

    def get(self, user_id: int) -> Optional[User]:
        """
        Get user by ID

        Args:
            user_id: User ID

        Returns:
            User or None
        """
        return self.repository.get(user_id)

    def get_by_email(self, email: str) -> Optional[User]:
        """
        Get user by email

        Args:
            email: User email

        Returns:
            User or None
        """
        return self.repository.get_by_email(email)

    def get_multi(self, skip: int = 0, limit: int = 100) -> List[User]:
        """
        Get multiple users

        Args:
            skip: Records to skip
            limit: Max records to return

        Returns:
            List of users
        """
        return self.repository.get_multi(skip=skip, limit=limit)

    def create(self, user_in: UserCreate) -> Optional[User]:
        """
        Create new user

        Args:
            user_in: User creation data

        Returns:
            Created user or None if email exists
        """
        # Check if email already exists
        if self.repository.email_exists(user_in.email):
            return None

        # Hash password
        hashed_password = get_password_hash(user_in.password)

        # Create user data
        user_data = {
            "email": user_in.email,
            "hashed_password": hashed_password,
            "full_name": user_in.full_name,
            "is_active": True,
            "is_superuser": False
        }

        # Create user
        return self.repository.create(user_data)

    def update(self, user_id: int, user_in: UserUpdate) -> Optional[User]:
        """
        Update user

        Args:
            user_id: User ID
            user_in: User update data

        Returns:
            Updated user or None
        """
        # Prepare update data
        update_data = {}

        if user_in.email is not None:
            # Check if new email already exists
            if self.repository.email_exists(user_in.email):
                return None
            update_data["email"] = user_in.email

        if user_in.password is not None:
            update_data["hashed_password"] = get_password_hash(user_in.password)

        if user_in.full_name is not None:
            update_data["full_name"] = user_in.full_name

        if user_in.is_active is not None:
            update_data["is_active"] = user_in.is_active

        # Update user
        return self.repository.update(user_id, update_data)

    def delete(self, user_id: int) -> bool:
        """
        Delete user

        Args:
            user_id: User ID

        Returns:
            True if deleted, False otherwise
        """
        return self.repository.delete(user_id)
