# import os
from typing import List
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from dataclasses import dataclass

# import boto3
# from botocore.exceptions import ClientError

# from app.core.config import settings
from app.domain.image.image_limits import ImageLimits
from app.core.cache import redis_client
from app.enums.storage_enum import StorageObjectTypeEnum
from app.enums.photo_enum import (
    PhotoCategoryEnum,
    PhotoProcessingStatusEnum,
    PhotoVisibilityEnum,
)
from app.models.user_model import UserModel
from app.models.photo_model import PhotoModel
from app.application.services.auth_service import AuthService
from app.services.property_service import PropertyService
from app.repositories.photo_repository import PhotoRepository
from app.core.exceptions.domain_exception import (
    PhotoNotFound,
    InvalidImageType,
    ImageTooLarge,
)
from app.infrastructure.storage.s3_service import S3Service


@dataclass
class PresignedUploadUrlData:
    method: str
    upload_url: str
    expires_at: datetime


@dataclass
class PresignedUploadUrlResult:
    photo_public_id: str
    upload: PresignedUploadUrlData


class PhotoService:

    # -----------------------------------------------
    # PRESIGNED
    # -----------------------------------------------

    @staticmethod
    def generate_presigned_upload_url(
        db: Session,
        storage: S3Service,
        property_public_id: str,
        category: PhotoCategoryEnum,
        content_type: str,
        file_size: int,
        current_user: UserModel | None = None,
    ) -> PresignedUploadUrlResult:

        PhotoService._validate_presigned_request(content_type, file_size)

        db_property = PropertyService.get_by_public_id_or_404(db, property_public_id, include_deleted=False)

        AuthService.ensure_owner_or_admin(db_property.user_id, current_user, "add photos", "property")

        photo = PhotoService.create(
            db=db,
            property_public_id=property_public_id,
            category=category,
            processing_status=PhotoProcessingStatusEnum.PENDING,
            visibility=PhotoVisibilityEnum.UNLISTED,
        )

        storage_key = PhotoService._build_photo_storage_key(
            property_public_id,
            photo.public_id,
            content_type,
            StorageObjectTypeEnum.ORIGINAL,
        )

        photo.storage_key = storage_key
        db.commit()
        db.refresh(photo)

        presigned_data: PresignedUploadUrlData = storage.generate_presigned_upload_url(
            storage_key=storage_key, content_type=content_type
        )

        return PresignedUploadUrlResult(photo.public_id, presigned_data)

    @staticmethod
    def get_presigned_read_url(db: Session, storage: S3Service, photo: PhotoModel) -> str:

        redis_key = f"photo_read_url:{photo.public_id}"
        cached_url = redis_client.get(redis_key)
        if cached_url:
            return cached_url

        presigned = storage.generate_presigned_read_url(storage_key=photo.storage_key)

        ttl_seconds = int((presigned.expires_at - datetime.now(timezone.utc)).total_seconds())
        redis_client.setex(redis_key, ttl_seconds, presigned.url)

        return presigned.url

    # -----------------------------------------------
    # CRUD - CREATE
    # -----------------------------------------------

    @staticmethod
    def create(
        db: Session,
        property_public_id: str,
        category: PhotoCategoryEnum,
        processing_status: PhotoProcessingStatusEnum,
        visibility: PhotoVisibilityEnum,
        position: int | None = None,
        file_url: str | None = None,
        thumbnail_url: str | None = None,
        is_cover: bool = False,
        is_active: bool = True,
    ) -> PhotoModel:

        # validar se existe a property?

        db_property = PropertyService.get_by_public_id_or_404(
            db, property_public_id, is_active=None, include_deleted=False
        )

        if position is None:
            existing_photos = PhotoRepository.list_by_property(db, db_property.id)
            position = len(existing_photos)

        if is_cover:
            pass  # definir o que será feito e se será setado como cover apenas apos processada

        photo = PhotoRepository.create(
            db=db,
            property_id=db_property.id,
            category=category,
            processing_status=processing_status,
            visibility=visibility,
            position=position,
            file_url=file_url,
            thumbnail_url=thumbnail_url,
            is_cover=is_cover,
            is_active=is_active,
        )

        db.commit()
        db.refresh(photo)

        return photo

    def mark_upload_completed(db: Session, photo_public_id: str, current_user: UserModel) -> PhotoModel:

        db_photo = PhotoService._get_by_public_id_or_404(db, photo_public_id, is_active=None, include_deleted=False)

        AuthService.ensure_owner_or_admin(db_photo.property_id, current_user, "mark upload", "photo")

        db_photo.processing_status = PhotoProcessingStatusEnum.UPLOADED
        db.commit()
        db.refresh(db_photo)

        return db_photo

    # -----------------------------------------------
    # CRUD - READ
    # -----------------------------------------------

    @staticmethod
    def _get_by_id_or_404(
        db: Session,
        id: int,
        is_active: bool | None = True,
        include_deleted: bool = False,
    ) -> PhotoModel | None:
        db_photo = PhotoRepository.get_by_id(db, id, is_active, include_deleted)

        if not db_photo:
            raise PhotoNotFound()

        return db_photo

    @staticmethod
    def _get_by_public_id_or_404(
        db: Session,
        public_id: str,
        is_active: bool | None = True,
        include_deleted: bool = False,
    ) -> PhotoModel | None:
        db_photo = PhotoRepository.get_by_public_id(db, public_id, is_active, include_deleted)

        if not db_photo:
            raise PhotoNotFound()

        return db_photo

    @staticmethod
    def list_by_property(db: Session, property_id: int, include_deleted: bool = False) -> List[PhotoModel]:
        return PhotoRepository.list_by_property(db, property_id)

    @staticmethod
    def list_all(
        db: Session,
        status: PhotoProcessingStatusEnum = PhotoProcessingStatusEnum.READY,
        limit: int = 50,
        offset: int = 0,
        is_active: bool | None = True,
        include_deleted: bool = False,
    ) -> List[PhotoModel]:

        return PhotoRepository.list_all(db, limit, offset, is_active, include_deleted)

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
    def restore(db: Session, public_id: str) -> PhotoModel | None:
        db_photo = PhotoService._get_by_public_id_or_404(db, public_id, is_active=None, include_deleted=True)

        if db_photo.deleted_at is None:
            return db_photo

        PhotoRepository.restore(db, id)
        if db_photo:
            db.commit()
            db.refresh(db_photo)
        return db_photo

    @staticmethod
    def activate(db: Session, public_id: str) -> PhotoModel | None:
        db_photo = PhotoService._get_by_public_id_or_404(db, public_id, is_active=False, include_deleted=False)

        db_photo.is_active = True

        db.commit()
        db.refresh(db_photo)
        return db_photo

    @staticmethod
    def deactivate(db: Session, public_id: str) -> PhotoModel | None:
        db_photo = PhotoService._get_by_public_id_or_404(db, public_id, is_active=True, include_deleted=False)

        db_photo.is_active = False

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

    @staticmethod
    def _validate_presigned_request(content_type: str, file_size: int):
        limits = ImageLimits.IMAGE_LIMITS.get(content_type)
        if not limits:
            raise InvalidImageType(content_type)

        max_file_size = limits["max_file_size"]
        if file_size > max_file_size:
            raise ImageTooLarge(content_type, max_file_size)

    @staticmethod
    def _get_file_extension(content_type: str) -> str:
        limits = ImageLimits.IMAGE_LIMITS.get(content_type.lower())
        return limits

    @staticmethod
    def _get_extension_from_mime(content_type: str) -> str:
        normalized = ImageLimits.normalize_mime(content_type)

        mime_to_ext = {
            "image/jpeg": "jpg",
            "image/png": "png",
            "image/webp": "webp",
            "image/heic": "heic",
            "image/heif": "heif",
        }

        return mime_to_ext.get(normalized, "bin")

    @staticmethod
    def _build_photo_storage_key(
        property_public_id: str,
        photo_public_id: str,
        content_type: str,
        variant: StorageObjectTypeEnum = StorageObjectTypeEnum.ORIGINAL,
    ) -> str:

        ext = PhotoService._get_extension_from_mime(content_type)
        return f"properties/{property_public_id}/photos/{photo_public_id}/{variant.value.upper()}.{ext.lower()}"

    @staticmethod
    def enrich_with_thumbnails(db: Session, storage: S3Service, photos: List[PhotoModel]) -> List[PhotoModel]:
        for photo in photos:
            presigned_url = PhotoService.get_presigned_read_url(db, storage, photo)
            photo.thumb_presigned_url = presigned_url

        return photos
