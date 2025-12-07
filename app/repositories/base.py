"""
Base repository with CRUD operations
"""
from typing import Generic, TypeVar, Type, Optional, List
from sqlalchemy.orm import Session
from app.models.base import BaseModel

ModelType = TypeVar("ModelType", bound=BaseModel)


class BaseRepository(Generic[ModelType]):
    """
    Base repository class with common CRUD operations
    """

    def __init__(self, model: Type[ModelType], db: Session):
        """
        Initialize repository with model and database session

        Args:
            model: SQLAlchemy model class
            db: Database session
        """
        self.model = model
        self.db = db

    def get(self, id: int) -> Optional[ModelType]:
        """
        Get a record by ID

        Args:
            id: Record ID

        Returns:
            Model instance or None if not found
        """
        return self.db.query(self.model).filter(self.model.id == id).first()

    def get_multi(
        self,
        skip: int = 0,
        limit: int = 100
    ) -> List[ModelType]:
        """
        Get multiple records with pagination

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of model instances
        """
        return self.db.query(self.model).offset(skip).limit(limit).all()

    def create(self, obj_in: dict) -> ModelType:
        """
        Create a new record

        Args:
            obj_in: Dictionary with model data

        Returns:
            Created model instance
        """
        db_obj = self.model(**obj_in)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def update(self, id: int, obj_in: dict) -> Optional[ModelType]:
        """
        Update a record

        Args:
            id: Record ID
            obj_in: Dictionary with updated data

        Returns:
            Updated model instance or None if not found
        """
        db_obj = self.get(id)
        if db_obj is None:
            return None

        for field, value in obj_in.items():
            if value is not None:
                setattr(db_obj, field, value)

        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def delete(self, id: int) -> bool:
        """
        Delete a record

        Args:
            id: Record ID

        Returns:
            True if deleted, False if not found
        """
        db_obj = self.get(id)
        if db_obj is None:
            return False

        self.db.delete(db_obj)
        self.db.commit()
        return True
