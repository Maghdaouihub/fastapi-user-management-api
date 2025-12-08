"""
User database model
"""
from sqlalchemy import Column, String, Boolean
from app.models.base import BaseModel


class User(BaseModel):
    """User model with authentication fields"""

    __tablename__ = "users"

    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, username={self.username})>"
