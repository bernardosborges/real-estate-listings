import enum

class PhotoVisibilityEnum(str, enum.Enum):
    PUBLIC = "public"
    PRIVATE = "private"
    UNLISTED = "unlisted"

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