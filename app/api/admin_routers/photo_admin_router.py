from typing import List
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session

from app.api.deps.general_deps import get_db_session, get_superuser, get_storage_service
from app.core.config import settings
from app.models.user_model import UserModel
from app.services.photo_admin_service import PhotoAdminService
from app.infrastructure.storage.s3_service import S3Service
from app.jobs.admin.dlq import reprocess_dlq_job
from app.schemas.photo_admin_schema import FailedPhotoResponseSchema



router = APIRouter(prefix=f"{settings.API_PREFIX}/admin/photos", tags=["Admin Photos"])


# -----------------------------------------------
# ADMIN ENDPOINT - REPROCESS
# -----------------------------------------------

@router.post(
        "/{public_id}/reprocess",
        status_code=status.HTTP_202_ACCEPTED,
        summary="Reprocess photo",
        description="Reprocess photo that failed."
)
def reprocess_photo_endpoint(
    public_id: str,
    db: Session = Depends(get_db_session),
    current_user: UserModel = Depends(get_superuser)
):
    PhotoAdminService.reprocess_photo(db, public_id, current_user)

    return {"message": "Photo reprocessing enqueued", "photo_public_id": public_id}



@router.get(
        "/failed",
        response_model=List[FailedPhotoResponseSchema],
        status_code=status.HTTP_200_OK,
        summary="Get failed photos",
        description="Retrieves a list of photos that failed."
)
def list_failed_photos_endpoint(
    limit: int = Query(50, ge=1, le=100, description="Maximum number of results"),
    offset: int = Query(0, ge=0, description="Number of results to skip"),
    db: Session = Depends(get_db_session),
    current_user: UserModel = Depends(get_superuser)
):
    return PhotoAdminService.list_failed_photos(db, limit, offset)
