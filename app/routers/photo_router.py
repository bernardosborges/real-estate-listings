from fastapi import APIRouter, Depends, HTTPException, status, Security, Query
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.config import settings
from app.core.oauth2 import get_current_user
from app.models.user_model import UserModel
from app.services.photo_service import PhotoService
from app.schemas.photo_schema import PhotoCreateSchema, PhotoReadSchema, PhotoUpdateSchema, PhotoPresignedUrlSchema


router = APIRouter(prefix=f"{settings.API_PREFIX}/photos", tags=["Photos"])


# -----------------------------------------------
# ENDPOINT - CREATE PHOTO
# -----------------------------------------------

@router.post(
        "/", 
        response_model=PhotoReadSchema,
        status_code=status.HTTP_201_CREATED,
        summary="Create a photo",
        description="Create a photo in the database."
)
def create_photo_endpoint(
    payload: PhotoCreateSchema,
    db: Session = Depends(get_db),
    current_user: UserModel = Security(get_current_user)
):
    return PhotoService.create(db, **payload.model_dump(exclude_unset=True))


@router.post(
        "/generate-upload-url", 
        response_model=PhotoPresignedUrlSchema,
        status_code=status.HTTP_201_CREATED,
        summary="Create url for photo upload",
        description="Create a pre-signed url for photo upload to the database."
)
def create_photo_upload_url_endpoint(
    payload: PhotoCreateSchema,
    db: Session = Depends(get_db),
    current_user: UserModel = Security(get_current_user)
):
    return PhotoService.create(db, **payload.model_dump(exclude_unset=True))


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
    db: Session = Depends(get_db),
    current_user: UserModel = Security(get_current_user)
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
    db: Session = Depends(get_db),
    current_user: UserModel = Security(get_current_user)
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
    db: Session = Depends(get_db),
    current_user: UserModel = Security(get_current_user)
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
    db: Session = Depends(get_db),
    current_user: UserModel = Security(get_current_user)
):
    return PhotoService.restore(db, photo_id)