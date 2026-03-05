from pydantic import BaseModel
from datetime import datetime

from app.enums.photo_enum import PhotoProcessingStatusEnum


class FailedPhotoResponseSchema(BaseModel):
    public_id: str
    processing_status: PhotoProcessingStatusEnum
    storage_key: str
    file_url: str | None
    thumbnail_url: str | None
    updated_at: datetime | None

    model_config = {
        "title": "FailedPhotoResponseSchema",
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "public_id": "9999-99999-99999-99",
                "processing_status": "FAILED",
                "file_url": "https://www.photolink.com/213123",
                "thumbnail_url": "https://www.photolink.com/213123",
                "updated_at": "2026-01-21T13:10:44Z",
            }
        },
    }
