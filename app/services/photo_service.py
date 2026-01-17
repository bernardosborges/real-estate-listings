from typing import List
from sqlalchemy.orm import Session
from datetime import datetime, timezone
import boto3
from botocore.exceptions import ClientError

from app.core.config import settings
from app.enums.photo_enum import PhotoCategoryEnum, PhotoProcessingStatusEnum, PhotoVisibilityEnum
from app.models.photo_model import PhotoModel
from app.repositories.photo_repository import PhotoRepository

class PhotoService:


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

        if position is None:
            existing_photos = PhotoRepository.list_by_property(db, property_id)
            position = len(existing_photos)
        
        if is_cover:
            pass # definir o que será feito e se será setado como cover apenas apos processada

        photo = PhotoRepository.create(
            db=db,
            property_id=property_id,
            category=category,
            processing_status=processing_status,
            visibility=visibility,
            position=position,
            file_url=file_url,
            thumbnail_url=thumbnail_url,
            is_cover=is_cover,
            is_active=is_active
        )
        
        db.commit()
        db.refresh(photo)

        return photo



    @staticmethod
    def generate_presigned_upload_url(
        db: Session,
        property_id: int,
        filename: str,
        file_type: str,
        is_cover: bool = False,
        expiration: int = 3600
    ) -> dict:
        return []
        

# -----------------------------------------------
# CRUD - READ
# -----------------------------------------------

    @staticmethod
    def get_by_id(db: Session, id: int, include_deleted: bool = False) -> PhotoModel | None:
        return PhotoRepository.get_by_id(db, id)

    @staticmethod
    def list_by_property(db: Session, property_id: int, include_deleted: bool = False) -> List[PhotoModel]:
        return PhotoRepository.list_by_property(db, property_id)


# -----------------------------------------------
# CRUD - UPDATE
# -----------------------------------------------

    @staticmethod
    def update(db: Session, id: int, **kwargs) -> PhotoModel | None:
        db_photo = PhotoRepository.update(db, id, **kwargs)
        if not db_photo:
            raise
        
        if db_photo:
            db.commit()
            db.refresh(db_photo)
        return db_photo


    @staticmethod
    def restore(db: Session, id: int) -> PhotoModel | None:
        db_photo = PhotoRepository.restore(db, id)
        if db_photo:
            db.commit()
            db.refresh(db_photo)
        return db_photo

# -----------------------------------------------
# CRUD - DELETE
# -----------------------------------------------

    @staticmethod
    def delete(db: Session, id: int, hard: bool = False) -> PhotoModel | None:
        db_photo = PhotoRepository.delete(db, id, hard)
        if db_photo:
            db.commit()
            db.refresh(db_photo)
        return db_photo
    

# -----------------------------------------------
# CRUD - UTILS
# -----------------------------------------------