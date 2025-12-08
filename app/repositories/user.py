"""
User repository with user-specific queries
"""
from typing import Optional
from sqlalchemy.orm import Session
from app.repositories.base import BaseRepository
from app.models.user import User


class UserRepository(BaseRepository[User]):
    """User repository with custom user queries"""

    def __init__(self, db: Session):
        super().__init__(User, db)

    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        return self.db.query(User).filter(User.email == email).first()

    def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        return self.db.query(User).filter(User.username == username).first()

    def get_active_users(self, skip: int = 0, limit: int = 100):
        """Get all active users"""
        return (
            self.db.query(User)
            .filter(User.is_active == True)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_superusers(self):
        """Get all superusers"""
        return self.db.query(User).filter(User.is_superuser == True).all()

    def authenticate(self, email: str, password: str) -> Optional[User]:
        """Authenticate user by email and password"""
        from app.core.security import verify_password

        user = self.get_by_email(email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_active(self, user: User) -> bool:
        """Check if user is active"""
        return user.is_active

    def is_superuser(self, user: User) -> bool:
        """Check if user is superuser"""
        return user.is_superuser
