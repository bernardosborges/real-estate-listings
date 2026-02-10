from typing import Dict, TypedDict
from app.core.exceptions.domain_exception import ImageLimitsError

class ImageLimit(TypedDict):
    max_file_size: int
    max_width: int
    max_height: int

class ImageLimits:

    IMAGE_LIMITS: Dict[str, ImageLimit] = {
        "image/jpeg": {
            "max_file_size": 15 * 1024 * 1024, #15 MB
            "max_width": 8000,
            "max_height": 8000,
        },
        "image/png": {
            "max_file_size": 10 * 1024 * 1024, #10 MB
            "max_width": 6000,
            "max_height": 6000,
        },
        "image/webp": {
            "max_file_size": 10 * 1024 * 1024,
            "max_width": 8000,
            "max_height": 8000,
        },
        "image/heic": {
            "max_file_size": 20 * 1024 * 1024, #iPhone
            "max_width": 8000,
            "max_height": 8000,
        },
        "image/heif": {
            "max_file_size": 20 * 1024 * 1024, 
            "max_width": 8000,
            "max_height": 8000,
        },
    }

    MIME_ALIASES = {
        "image/jpg": "image/jpeg",
        "image/pjpeg": "image/jpeg",
        "image/x-jpeg": "image/jpeg",

        "image/heic-sequence": "image/heic",
        "image/heif-sequence": "image/heif",
    }

    @staticmethod
    def normalize_mime(content_type: str) -> str:
        normalized = content_type.lower().strip()

        # Strip parameters like "; chatset-binary"
        if ";" in normalized:
            normalized = normalized.split(";",1)[0]

        # Alias map
        if normalized in ImageLimits.MIME_ALIASES:
            return ImageLimits.MIME_ALIASES[normalized]

        # Family fallback (safe)
        if normalized.startswith("image/jpeg"):
            return "image/jpeg"
        if normalized.startswith("image/heic"):
            return "image/heic"
        if normalized.startswith("image/heif"):
            return "image/heif"
        
        return normalized

    @staticmethod
    def get_limits_for_mime(content_type: str) -> ImageLimit:
        normalized = ImageLimits.normalize_mime(content_type)
        limits = ImageLimits.IMAGE_LIMITS.get(normalized)
        if limits is not None:
            return limits
        else:
            raise ImageLimitsError(f"No limits defined for MIME {normalized}.")