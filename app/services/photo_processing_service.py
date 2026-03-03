import logging

from io import BytesIO
from dataclasses import dataclass
from PIL import Image
from sqlalchemy.orm import Session

from app.core.cache import redis_client
from app.infrastructure.storage.s3_service import S3Service
from app.models.photo_model import PhotoModel
from app.services.photo_service import PhotoService
from app.enums.photo_enum import PhotoProcessingStatusEnum
from app.domain.image.image_limits import ImageLimits
from app.domain.image.image_validator import ImageValidator
from app.domain.image.image_processor import ImageProcessor
from app.core.exceptions.domain_exception import (
    ImageExtensionError,
    ImageMimeError,
    ImageFileSizeError,
    ImageVerificationError,
    ImageDimensionsError,
)

logger = logging.getLogger(__name__)


class PhotoProcessingService:

    # -----------------------------------------------
    # ALL
    # -----------------------------------------------

    def __init__(self, db: Session, storage: S3Service, redis):
        self.db = db
        self.storage = storage
        self.redis = redis

    def process(self, photo_public_id: str) -> None:
        db_photo = PhotoService._get_by_public_id_or_404(
            self.db, photo_public_id, is_active=None, include_deleted=False
        )

        # Idempotency guard
        if db_photo.processing_status != PhotoProcessingStatusEnum.PENDING:
            logger.info(
                "Skipping photo processing - invalid state",
                extra={"photo": photo_public_id, "status": db_photo.processing_status},
            )
            self.redis.incr("metrics:photo.jobs.skipped")
            return

        self._mark_processing(db_photo)
        image = None

        try:
            ImageValidator.validate_extension(db_photo.storage_key)
            raw_bytes = self.storage.get_object_bytes(db_photo.storage_key)
            mime = ImageValidator.validate_and_detect_mime(
                raw_bytes, ImageLimits.IMAGE_LIMITS
            )
            limits: dict = ImageLimits.get_limits_for_mime(mime)
            ImageValidator.validate_file_size(raw_bytes, limits["max_file_size"])
            image = ImageValidator.validate_and_normalize_image_with_pil(raw_bytes)
            width, height = ImageValidator.validate_and_extract_image_dimensions(
                image, limits["max_width"], limits["max_height"]
            )
            processed = ImageProcessor.create_optimized_and_thumb(image)

            # Generate storage keys
            optimized_key = (
                db_photo.storage_key.replace("/ORIGINAL", "/OPTIMIZED").rsplit(".", 1)[
                    0
                ]
                + ".webp"
            )
            thumb_key = (
                db_photo.storage_key.replace("/ORIGINAL", "/THUMBNAIL").rsplit(".", 1)[
                    0
                ]
                + ".webp"
            )

            # Save optimized photo and thumbnail to storage
            self.storage.put_object_bytes(
                optimized_key, processed.optimized, content_type="image/webp"
            )
            self.storage.put_object_bytes(
                thumb_key, processed.thumbnail, content_type="image/webp"
            )

            self._mark_ready(db_photo, optimized_key, thumb_key, width, height)

            redis_client.delete(f"photo_read_url:{db_photo.public_id}")

            logger.info(f"Photo {photo_public_id} processed successfully.")

        except ImageExtensionError as exc:
            self.db.rollback()
            self._mark_failed(
                db_photo, f"Photo {photo_public_id} failed extension check: {exc}."
            )
            return  # Using return instead of raise to not retry the processes

        except ImageMimeError as exc:
            self.db.rollback()
            self._mark_failed(
                db_photo, f"Photo {photo_public_id} failed MIME/magic check: {exc}."
            )
            return  # Using return instead of raise to not retry the processes

        except ImageFileSizeError as exc:
            self.db.rollback()
            self._mark_failed(
                db_photo, f"Photo {photo_public_id} exceeds max file size: {exc}."
            )
            return  # Using return instead of raise to not retry the processes

        except ImageVerificationError as exc:
            self.db.rollback()
            self._mark_failed(
                db_photo, f"Photo {photo_public_id} failed MIME/magic check: {exc}."
            )
            return  # Using return instead of raise to not retry the processes

        except ImageDimensionsError as exc:
            self.db.rollback()
            self._mark_failed(
                db_photo, f"Photo {photo_public_id} failed image dimesion check: {exc}."
            )
            return  # Using return instead of raise to not retry the processes

        except Exception as exc:
            self.db.rollback()
            logger.exception(
                "Unexpected error during photo processing.",
                extra={"photo": photo_public_id},
            )
            raise  # Use raise for running a retry on the process

        finally:
            if image:
                image.close()

    def _mark_processing(self, photo: PhotoModel) -> None:
        photo.processing_status = PhotoProcessingStatusEnum.PROCESSING
        self.db.commit()

    def _mark_ready(
        self,
        photo: PhotoModel,
        optimized_key: str,
        thumb_key: str,
        width: int,
        height: int,
    ) -> None:
        photo.processing_status = PhotoProcessingStatusEnum.READY
        photo.file_url = optimized_key
        photo.thumbnail_url = thumb_key
        photo.width = width
        photo.height = height
        self.db.commit()

    def _mark_failed(self, photo: PhotoModel, reason: str) -> None:
        photo.processing_status = PhotoProcessingStatusEnum.FAILED
        self.db.commit()
        logger.warning(
            "Photo failed.", extra={"photo": photo.public_id, "reason": reason}
        )
