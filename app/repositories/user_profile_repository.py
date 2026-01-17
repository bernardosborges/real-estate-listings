from sqlalchemy import String
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timezone

from app.models.user_profile_model import UserProfileModel
from app.core.exceptions.domain_exception import UserProfileNotFound


class UserProfileRepository:

# -----------------------------------------------
# CRUD - CREATE
# -----------------------------------------------

    @staticmethod
    def create(db: Session, user_id: int, public_id: str) -> UserProfileModel:
        
        db_user_profile = UserProfileModel(user_id=user_id, public_id=public_id)
        
        try:
            db.add(db_user_profile)
            db.flush()
            return db_user_profile
        except IntegrityError:
            db.rollback()
            raise


# -----------------------------------------------
# CRUD - READ
# -----------------------------------------------

    @staticmethod
    def get_by_id(db: Session, id: int, include_deleted: bool = False) -> UserProfileModel | None:
        query = db.query(UserProfileModel).filter(UserProfileModel.id == id)
        if not include_deleted:
            query = query.filter(UserProfileModel.deleted_at.is_(None))

        return query.first()

    @staticmethod
    def get_by_public_id(db: Session, public_id: str, include_deleted: bool = False) -> UserProfileModel | None:
        query = db.query(UserProfileModel).filter(UserProfileModel.public_id == public_id)
        if not include_deleted:
            query = query.filter(UserProfileModel.deleted_at.is_(None))

        return query.first()
    
    @staticmethod
    def get_by_user_id(db: Session, user_id: int, include_deleted: bool = False) -> UserProfileModel | None:
        query = db.query(UserProfileModel).filter(UserProfileModel.user_id == user_id)
        if not include_deleted:
            query = query.filter(UserProfileModel.deleted_at.is_(None))

        return query.first()


# -----------------------------------------------
# CRUD - UPDATE
# -----------------------------------------------

    @staticmethod
    def update(db: Session, id: int, **kwargs) -> UserProfileModel | None:
        db_user_profile = UserProfileRepository.get_by_id(db, id)
        if not db_user_profile:
            return None

        for key, value in kwargs.items():
            setattr(db_user_profile, key, value)
        return db_user_profile

    @staticmethod
    def restore(db: Session, id: int) -> UserProfileModel | None:
        db_user_profile = UserProfileRepository.get_by_id(db, id, include_deleted=True)
        if not db_user_profile:
            return None

        db_user_profile.deleted_at = None

        return db_user_profile


# -----------------------------------------------
# CRUD - DELETE
# -----------------------------------------------

    @staticmethod
    def soft_delete(db: Session, id: int) -> UserProfileModel | None:
        return UserProfileRepository.delete(db, id, hard=False)
    
    @staticmethod
    def hard_delete(db: Session, id: int) -> UserProfileModel | None:
        return UserProfileRepository.delete(db, id, hard=True)

    @staticmethod
    def delete(db: Session, id: int, hard: bool = False) -> UserProfileModel | None:
        db_user_profile = UserProfileRepository.get_by_id(db, id)
        if not db_user_profile:
            return None
        
        if hard:
            db.delete(db_user_profile)
        else:
            db_user_profile.deleted_at = datetime.now(timezone.utc)

        return db_user_profile