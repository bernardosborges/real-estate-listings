import logging

from io import BytesIO
from dataclasses import dataclass
from PIL import Image

THUMB_SIZE = (400,400)
WEBP_QUALITY = 85


@dataclass
class ProcessedImages:
    optimized: BytesIO
    thumbnail: BytesIO

class ImageProcessor:

    @staticmethod
    def create_optimized_and_thumb(image: Image.Image) -> ProcessedImages:
        # Optimize and convert to WEBP
        optimized = BytesIO()
        image.save(optimized, format="WEBP", quality=WEBP_QUALITY, optimize=True)
        optimized.seek(0)

        # Create thumb
        thumbnail_image = image.copy()
        thumbnail_image.thumbnail(THUMB_SIZE)
        thumbnail = BytesIO()
        thumbnail_image.save(thumbnail, format="WEBP", optimize=True)
        thumbnail.seek(0)

        return ProcessedImages(optimized=optimized, thumbnail=thumbnail)
