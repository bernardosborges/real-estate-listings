from typing import List
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.photo_model import PhotoModel
from app.enums.photo_enum import PhotoCategoryEnum, PhotoProcessingStatusEnum, PhotoVisibilityEnum


class PhotoRepository:

# -----------------------------------------------
# CRUD - CREATE
# -----------------------------------------------

    @staticmethod
    def create(
        db: Session,
        property_id: int,
        category: PhotoCategoryEnum,
        processing_status: PhotoProcessingStatusEnum,
        visibility: PhotoVisibilityEnum,
        position: int,
        file_url: str | None = None,
        thumbnail_url: str | None = None,
        is_cover: bool = False,
        is_active: bool = True
    ) -> PhotoModel:
        
        photo = PhotoModel(
            property_id = property_id,
            file_url = file_url,
            thumbnail_url = thumbnail_url,
            category = category,
            visibility = visibility,
            processing_status = processing_status,
            position = position,
            is_cover = is_cover,
            is_active = is_active
        )

        db.add(photo)
        return photo



# -----------------------------------------------
# CRUD - READ
# -----------------------------------------------

    @staticmethod
    def get_by_id(db: Session, id: int, include_deleted: bool = False) -> PhotoModel | None:
        query = db.query(PhotoModel).filter(PhotoModel.id == id)

        if not include_deleted:
            query = query.filter(PhotoModel.deleted_at.is_(None))
        return query.first()

    @staticmethod    
    def get_cover(db: Session, property_id: int, include_deleted: bool = False) -> PhotoModel | None:
        query = db.query(PhotoModel).filter(PhotoModel.property_id == property_id, PhotoModel.is_cover == True)

        if not include_deleted:
            query = query.filter(PhotoModel.deleted_at.is_(None))
        return query.first()

    @staticmethod    
    def list_by_property(db: Session, property_id: int, include_deleted: bool = False) -> List[PhotoModel]:
        query = db.query(PhotoModel).filter(PhotoModel.property_id == property_id)

        if not include_deleted:
            query = query.filter(PhotoModel.deleted_at.is_(None))
        return query.all()


# -----------------------------------------------
# CRUD - UPDATE
# -----------------------------------------------

    @staticmethod
    def update(db: Session, id: int, **kwargs) -> PhotoModel | None:
        db_photo = PhotoRepository.get_by_id(db, id)
        if not db_photo:
            return None
        
        for key, value in kwargs.items():
            setattr(db_photo, key, value)
        return db_photo
         

    @staticmethod
    def restore(db: Session, id: int) -> PhotoModel | None:
        db_photo = PhotoRepository.get_by_id(db, id, include_deleted=True)
        if not db_photo:
            return None

        db_photo.deleted_at = None

        return db_photo

# -----------------------------------------------
# CRUD - DELETE
# -----------------------------------------------

    @staticmethod
    def delete(db: Session, id: int, hard: bool = False) -> PhotoModel | None:
        db_photo = PhotoRepository.get_by_id(db, id)
        if not db_photo:
            return None
        
        if hard:
            db.delete(db_photo)
        else:
            db_photo.deleted_at = datetime.now(timezone.utc)
            db_photo.is_active = False

        return db_photo
    
    @staticmethod
    def soft_delete(db: Session, id: int) -> PhotoModel | None:
        return PhotoRepository.delete(db, id, hard=False)
    
    @staticmethod
    def hard_delete(db: Session, id: int) -> PhotoModel | None:
        return PhotoRepository.delete(db, id, hard=True)
