from io import BytesIO
from typing import Set, Tuple

import magic
from PIL import Image, UnidentifiedImageError

from app.domain.image.image_limits import ImageLimits
from app.core.exceptions.domain_exception import ImageExtensionError, ImageMimeError, ImageFileSizeError, ImageVerificationError, ImageDimensionsError

ALLOWED_EXTENSIONS: Set[str] = {"jpg", "jpeg", "png", "webp", "heic", "heif"}

class ImageValidator:

    @staticmethod
    def validate_extension(storage_key: str) -> None:
        ext = storage_key.lower().split('.')[-1]
        if ext not in ALLOWED_EXTENSIONS:
            raise ImageExtensionError(f"Invalid file extension: {ext}")

    @staticmethod
    def validate_file_size(raw_bytes: bytes, max_file_size: int) -> None:
        max_mb = round(max_file_size / (1024 * 1024), 1)
        if len(raw_bytes) > max_file_size:
            raise ImageFileSizeError(f"File exceeds max size: {max_file_size} ({max_mb} MB).")

    @staticmethod
    def validate_and_detect_mime(raw_bytes: bytes, valid_types: dict) -> str:
        raw_mime = magic.from_buffer(raw_bytes, mime=True)
        mime = ImageLimits.normalize_mime(raw_mime)
        if mime not in valid_types:
            raise ImageMimeError(f"Unsupported MIME type: {mime}")
        return mime

    @staticmethod
    def validate_and_normalize_image_with_pil(raw_bytes: bytes) -> Image.Image:
        try:
            with BytesIO(raw_bytes) as bio:
                image = Image.open(bio)
                image.verify()

            image = Image.open(BytesIO(raw_bytes))
            if image.mode not in ("RGB",):
                    image = image.convert("RGB")
            return image

        except UnidentifiedImageError as exc:
            raise ImageVerificationError(f"Invalid image file.") from exc

    @staticmethod
    def validate_and_extract_image_dimensions(image: Image.Image, max_width: int, max_height: int) -> Tuple[int, int]:
        width, height = image.size
        if width > max_width or height > max_height:
            raise ImageDimensionsError(f"Image dimensions ({width}x{height}) exceed limits ({max_width}x{max_height}).")
        return width, height
