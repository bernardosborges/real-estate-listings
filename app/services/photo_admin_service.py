import logging
from sqlalchemy.orm import Session

from app.models.user_model import UserModel
from app.models.photo_model import PhotoModel
from app.repositories.photo_repository import PhotoRepository
from app.services.photo_service import PhotoService
from app.enums.photo_enum import PhotoProcessingStatusEnum
from app.jobs.enqueue import enqueue_photo_processing
from app.core.exceptions.domain_exception import PhotoProcessConflict

logger = logging.getLogger(__name__)

class PhotoAdminService:

    @staticmethod
    def reprocess_photo(db: Session, public_id: str, current_user: UserModel) -> None:
        rows = PhotoRepository.atomic_mark_pending_if_failed(db, public_id)
        if rows == 0:
            raise PhotoProcessConflict(f"Photo cannot be reprocessed. public_id: {public_id}")

        db.commit()
        enqueue_photo_processing(public_id)
        logger.warning("Admin triggered photo reprocess", extra={"photo_public_id": public_id, "admin_user_id": current_user.id,},)
        

    @staticmethod
    def list_failed_photos(db: Session, limit: int = 50, offset: int = 0) -> list[PhotoModel]:
        return PhotoService.list_all(db, PhotoProcessingStatusEnum.FAILED, limit, offset, is_active=None, include_deleted=True)
