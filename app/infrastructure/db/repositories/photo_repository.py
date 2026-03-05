from typing import List
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.models.photo_model import PhotoModel
from app.enums.photo_enum import (
    PhotoCategoryEnum,
    PhotoProcessingStatusEnum,
    PhotoVisibilityEnum,
)


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
        is_active: bool = True,
    ) -> PhotoModel:

        photo = PhotoModel(
            property_id=property_id,
            file_url=file_url,
            thumbnail_url=thumbnail_url,
            category=category,
            visibility=visibility,
            processing_status=processing_status,
            position=position,
            is_cover=is_cover,
            is_active=is_active,
        )

        db.add(photo)
        return photo

    # -----------------------------------------------
    # CRUD - READ
    # -----------------------------------------------

    @staticmethod
    def get_by_id(
        db: Session,
        id: int,
        is_active: bool | None = True,
        include_deleted: bool = False,
    ) -> PhotoModel | None:
        query = db.query(PhotoModel).filter(PhotoModel.id == id)

        if is_active is not None:
            query = query.filter(PhotoModel.is_active == is_active)

        if not include_deleted:
            query = query.filter(PhotoModel.deleted_at.is_(None))
        return query.first()

    @staticmethod
    def get_by_public_id(
        db: Session,
        public_id: str,
        is_active: bool | None = True,
        include_deleted: bool = False,
    ) -> PhotoModel | None:
        query = db.query(PhotoModel).filter(PhotoModel.public_id == public_id)

        if is_active is not None:
            query = query.filter(PhotoModel.is_active == is_active)

        if not include_deleted:
            query = query.filter(PhotoModel.deleted_at.is_(None))
        return query.first()

    @staticmethod
    def get_cover(db: Session, property_id: int, include_deleted: bool = False) -> PhotoModel | None:
        query = db.query(PhotoModel).filter(PhotoModel.property_id == property_id, PhotoModel.is_cover)

        if not include_deleted:
            query = query.filter(PhotoModel.deleted_at.is_(None))
        return query.first()

    @staticmethod
    def list_by_property(
        db: Session,
        public_id: str,
        is_active: bool | None = True,
        include_deleted: bool = False,
    ) -> List[PhotoModel]:
        query = db.query(PhotoModel).filter(PhotoModel.property_id == public_id)

        if is_active is not None:
            query = query.filter(PhotoModel.is_active == is_active)

        if not include_deleted:
            query = query.filter(PhotoModel.deleted_at.is_(None))
        return query.all()

    @staticmethod
    def list_all(
        db: Session,
        status: PhotoProcessingStatusEnum = PhotoProcessingStatusEnum.READY,
        limit: int = 50,
        offset: int = 0,
        is_active: bool | None = True,
        include_deleted: bool = False,
    ) -> List[PhotoModel]:

        query = db.query(PhotoModel).filter(PhotoModel.processing_status == status)

        if is_active is not None:
            query = query.filter(PhotoModel.is_active == is_active)

        if not include_deleted:
            query = query.filter(PhotoModel.deleted_at.is_(None))

        query.order_by(PhotoModel.updated_at.desc())

        return query.offset(offset).limit(limit).all()

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

    @staticmethod
    def atomic_mark_pending_if_failed(db: Session, public_id: str) -> int:
        """
        Atomically: FAILED -> PENDING Returns: number of affected rows (0 or 1)
        """
        return (
            db.query(PhotoModel)
            .filter(
                PhotoModel.public_id == public_id,
                PhotoModel.processing_status == PhotoProcessingStatusEnum.FAILED,
            )
            .update(
                {
                    PhotoModel.processing_status: PhotoProcessingStatusEnum.PENDING,
                    PhotoModel.file_url: None,
                    PhotoModel.thumbnail_url: None,
                    PhotoModel.width: None,
                    PhotoModel.height: None,
                },
                synchronize_session=False,
            )
        )

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
