from __future__ import annotations
import enum

class PhotoVisibilityEnum(str, enum.Enum):
    PUBLIC = "public" # everyone see
    PRIVATE = "private" # logged see
    UNLISTED = "unlisted" # owner and superadmin see

class PhotoProcessingStatusEnum(str, enum.Enum):
    PENDING = "pending"
    UPLOADED = "uploaded"
    PROCESSING = "processing"
    READY = "ready"
    FAILED = "failed"

class PhotoCategoryEnum(str, enum.Enum):

    # EXTERNAL
    FACADE = "facade"
    EXTERIOR = "exterior"
    STREET_VIEW = "street_view"
    AERIAL = "aerial"
    MAP = "map"

    # INTERNAL
    INTERNAL = "internal"

    # COMUM AREA
    AMENITIES = "amenities"

    # PROJECT
    FLOORPLAN = "floorplan"
    RENDER = "render"

    # OTHERS
    DOCUMENT = "document"
    GENERAL ="general"

    @classmethod
    def from_str(cls, str: str) -> PhotoCategoryEnum:
        if not isinstance(str, str):
            raise InvalidPhotoCategory()

        try:
            return cls(str.upper())
        except ValueError:
            raise InvalidPhotoCategory()
