from pydantic import BaseModel, HttpUrl, Field
from datetime import datetime
from uuid import UUID
from typing import Literal
from typing import cast

from app.enums.photo_enum import PhotoCategoryEnum, PhotoProcessingStatusEnum, PhotoVisibilityEnum

# -----------------------------------------------
# BASE
# -----------------------------------------------


class PhotoBaseSchema(BaseModel):
    id: int
    file_url: str
    thumbnail_url: str

    model_config = {
        "title": "PhotoBaseSchema",
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 1,
                "file_url": "https://www.photolink.com/213123",
                "thumbnail_url": "https://www.photolink.com/213123",
            }
        },
    }


# -----------------------------------------------
# PRESIGNED URL REQUEST & RESPONSE
# -----------------------------------------------


class PhotoPresignedUrlUploadRequestSchema(BaseModel):
    category: PhotoCategoryEnum
    content_type: Literal["image/jpeg", "image/png", "image/webp", "image/heic", "image/heif"]
    file_size: int = Field(..., gt=0, description="File size in bytes")


class PhotoPresignedUrlUploadDataSchema(BaseModel):
    method: Literal["PUT"]
    upload_url: HttpUrl
    expires_at: datetime


class PhotoPresignedUrlUploadResponseSchema(BaseModel):
    photo_public_id: UUID
    upload: PhotoPresignedUrlUploadDataSchema


class PhotoMarkUploadedResponseSchema(BaseModel):
    photo_public_id: UUID
    status: PhotoProcessingStatusEnum


# -----------------------------------------------
# CREATE
# -----------------------------------------------


class PhotoCreateSchema(BaseModel):
    file_url: str
    thumbnail_url: str

    model_config = {
        "title": "PhotoBaseSchema",
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "file_url": "https://www.photolink.com/213123",
                "thumbnail_url": "https://www.photolink.com/213123",
            }
        },
    }


# -----------------------------------------------
# READ
# -----------------------------------------------


class PhotoThumbnailResponseSchema(BaseModel):
    public_id: str
    thumb_presigned_url: str | None
    category: PhotoCategoryEnum
    position: int
    width: int | None
    height: int | None

    model_config = {
        "title": "PhotoReadSchema",
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "thumb_presigned_url": "https://www.photolink.com/213123",
                "category": PhotoCategoryEnum.FACADE,
                "position": 28,
                "width": 300,
                "height": 400,
            }
        },
    }


class PhotoReadSchema(BaseModel):
    public_id: str
    file_url: str
    thumbnail_url: str | None
    category: PhotoCategoryEnum
    position: int
    width: int | None
    height: int | None

    is_cover: bool

    model_config = {
        "title": "PhotoReadSchema",
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "file_url": "https://www.photolink.com/213123",
                "thumbnail_url": "https://www.photolink.com/213123",
                "category": "facade",
                "position": "28",
                "width": 300,
                "height": 400,
                "is_cover": False,
            }
        },
    }


class PhotoReadEditSchema(PhotoReadSchema):
    visibility: PhotoVisibilityEnum
    model_config = {
        "title": "PhotoReadSchema",
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                **cast(dict, PhotoReadSchema.model_config)["json_schema_extra"]["example"],
                "visibility": PhotoVisibilityEnum.PUBLIC,
            }
        },
    }


# -----------------------------------------------
# UPDATE
# -----------------------------------------------


class PhotoUpdateSchema(BaseModel):
    category: PhotoCategoryEnum | None
    visibility: PhotoVisibilityEnum | None
    position: int | None
    is_cover: bool | None

    model_config = {
        "title": "PhotoUpdateSchema",
        "from_attributes": True,
        "json_schema_extra": {
            "example": {"category": "facade", "visibility": "public", "position": "28", "is_cover": True}
        },
    }
