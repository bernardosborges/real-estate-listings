from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List

from app.api.deps.general_deps import get_db_session, get_authenticated_user, get_storage_service
from app.core.config import settings
from app.models.user_model import UserModel
from app.services.photo_service import PhotoService
from app.infrastructure.storage.s3_service import S3Service
from app.schemas.photo_schema import PhotoCreateSchema, PhotoReadSchema, PhotoUpdateSchema, PhotoPresignedUrlUploadRequestSchema, PhotoPresignedUrlUploadResponseSchema, PhotoMarkUploadedResponseSchema


router = APIRouter(prefix=f"{settings.API_PREFIX}/photos", tags=["Photos"])


# -----------------------------------------------
# ENDPOINT - CREATE PHOTO
# -----------------------------------------------

@router.post(
        "/{property_public_id}/presigned-url", 
        response_model=PhotoPresignedUrlUploadResponseSchema,
        status_code=status.HTTP_201_CREATED,
        summary="Create url for photo upload",
        description="Create a pre-signed url for photo upload to the database."
)
def create_photo_presigned_upload_url_endpoint(
    payload: PhotoPresignedUrlUploadRequestSchema,
    property_public_id: str,
    db: Session = Depends(get_db_session),
    storage: S3Service = Depends(get_storage_service),
    current_user: UserModel = Depends(get_authenticated_user)
):
    return PhotoService.generate_presigned_upload_url(db, storage, property_public_id, **payload.model_dump(exclude_unset=True), current_user=current_user)


@router.post(
        "/{photo_public_id}/mark-uploaded", 
        response_model=PhotoMarkUploadedResponseSchema,
        status_code=status.HTTP_200_OK,
        summary="Mark photo upload as completed",
        description="Notify backend that the photo has been uploaded to the storage."
)
def mark_photo_uploaded_endpoint(
    photo_public_id: str,
    db: Session = Depends(get_db_session),
    current_user: UserModel = Depends(get_authenticated_user)
):
    db_photo = PhotoService.mark_upload_completed(db, photo_public_id, current_user)
    return PhotoMarkUploadedResponseSchema(photo_public_id=db_photo.public_id, status=db_photo.processing_status.value)


# -----------------------------------------------
# ENDPOINT - GET PHOTO
# -----------------------------------------------

@router.get(
        "/{photo_id}", 
        response_model=PhotoReadSchema,
        summary="Get a photo",
        description="Get a photo from the database."
)
def get_photo_by_id_endpoint(
    photo_id: int,
    db: Session = Depends(get_db_session),
    current_user: UserModel = Depends(get_authenticated_user)
):
    return PhotoService.get_by_id(db, photo_id)


# -----------------------------------------------
# ENDPOINT - LIST PHOTOS
# -----------------------------------------------

@router.get(
        "/property/{property_id}", 
        response_model=List[PhotoReadSchema],
        summary="List photos of a property",
        description="List all photos of a property from the database."
)
def list_photo_by_property_endpoint(
    property_id: int,
    db: Session = Depends(get_db_session),
    current_user: UserModel = Depends(get_authenticated_user)
):
    return PhotoService.list_by_property(db, property_id)

# -----------------------------------------------
# ENDPOINT - UPDATE PHOTO
# -----------------------------------------------

@router.patch(
        "/{photo_id}", 
        response_model=PhotoReadSchema,
        summary="Update a photo.",
        description="Updates a photo to the database."
)
def update_photo_endpoint(
    photo_id: int,
    payload: PhotoUpdateSchema,
    db: Session = Depends(get_db_session),
    current_user: UserModel = Depends(get_authenticated_user)
):
    if photo_id != payload.id:
        raise 
    return PhotoService.update(db, **payload.model_dump(exclude_unset=True))


@router.patch(
        "/{photo_id}/restore", 
        response_model=PhotoReadSchema,
        summary="Restore a photo",
        description="Restores a photo to the database."
)
def restore_photo_endpoint(
    photo_id: int,
    db: Session = Depends(get_db_session),
    current_user: UserModel = Depends(get_authenticated_user)
):
    return PhotoService.restore(db, photo_id)