"""
Database base module
Imports all models for Alembic migrations
"""
from app.db.session import Base

# Import all models here for Alembic to detect them
from app.models.user import User

__all__ = ["Base", "User"]
