from pydantic import BaseModel
from datetime import datetime, timezone

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
                "thumbnail_url": "https://www.photolink.com/213123"
            }
        }
    }


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
                "thumbnail_url": "https://www.photolink.com/213123"
            }
        }
    }


# -----------------------------------------------
# READ
# -----------------------------------------------

class PhotoReadSchema(BaseModel):
    property_id: int
    file_url: str
    thumbnail_url: str
    category: PhotoCategoryEnum
    visibility: PhotoVisibilityEnum
    processing_status: PhotoProcessingStatusEnum
    position: int
    width: int
    height: int

    is_cover: bool


    model_config = {
        "title": "PhotoReadSchema",
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "property_id": 103,
                "file_url": "https://www.photolink.com/213123",
                "thumbnail_url": "https://www.photolink.com/213123",
                "category": "facade",
                "visibility": "public",
                "processing_status": "ready",
                "position": "28",
                "width": 300,
                "height": 400
            }
        }
    }

class PhotoPresignedUrlSchema(BaseModel):

    model_config = {
        "title": "PhotoPresignedUrlSchema",
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
            }
        }
    }

# -----------------------------------------------
# UPDATE
# -----------------------------------------------

class PhotoUpdateSchema(BaseModel):
    property_id: int
    category: PhotoCategoryEnum
    visibility: PhotoVisibilityEnum
    processing_status: PhotoProcessingStatusEnum
    position: int
    is_cover: bool
    file_url: str | None = None
    thumbnail_url: str | None = None
    width: int | None = None
    height: int | None = None

    model_config = {
        "title": "PhotoUpdateSchema",
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "property_id": 103,
                "category": "facade",
                "visibility": "public",
                "processing_status": "ready",
                "position": "28",
                "file_url": "https://www.photolink.com/213123",
                "thumbnail_url": "https://www.photolink.com/213123",
                "width": 300,
                "height": 400
            }
        }
    }