from fastapi import status

class DomainException(Exception):
    status_code: int = status.HTTP_400_BAD_REQUEST
    error_code: str = "DOMAIN_ERROR"
    message: str = "Domain error"

    def __init__(self, message: str | None = None):
        super().__init__(message or self.message)


# -----------------------------------------------
# AUTHENTICATION
# -----------------------------------------------





# -----------------------------------------------
# PROPERTY
# -----------------------------------------------





# -----------------------------------------------
# PROPERTY TAG
# -----------------------------------------------

class PropertyTagNotFound(DomainException):
    status_code = status.HTTP_404_NOT_FOUND
    error_code = "PROPERTY_TAG_NOT_FOUND"
    message = "Property tag not found"

# -----------------------------------------------
# TAGS
# -----------------------------------------------

class TagAlreadyExists(DomainException):
    status_code = status.HTTP_404_NOT_FOUND
    error_code = "TAG_ALREADY_EXISTS"
    message = "Tag already exists"

class TagNotFound(DomainException):
    status_code = status.HTTP_404_NOT_FOUND
    error_code = "TAG_NOT_FOUND"
    message = "Tag not found"

    def __init__(self, id: int | None = None, slug: str | None = None):
        self.id = id
        self.slug = slug
        super().__init__(f"Tag {id}{slug} not found")

# -----------------------------------------------
# TAGS GROUP
# -----------------------------------------------

class TagGroupAlreadyExists(DomainException):
    status_code = status.HTTP_409_CONFLICT
    error_code = "TAG_GROUP_ALREADY_EXISTS"
    message = "Tag group already exists"

class TagGroupNotFound(DomainException):
    status_code = status.HTTP_404_NOT_FOUND
    error_code = "TAG_GROUP_NOT_FOUND"
    message = "Tag group not found"

    def __init__(self, id: int | None = None, slug: str | None = None):
        self.id = id
        self.slug = slug

        if id is not None:
            message = f"TagGroup with id={id} not found"
        elif slug is not None:
            message = f"TagGroup with slug='{slug}' not found"
        else:
            message = "TagGroup not found"

        super().__init__(message)

# -----------------------------------------------
# PHOTO
# -----------------------------------------------

class PhotoNotFound(DomainException):
    status_code = status.HTTP_404_NOT_FOUND
    error_code = "PHOTO_NOT_FOUND"
    message = "Photo not found"

class InvalidImageType(DomainException):
    status_code = status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
    error_code = "INVALID_IMAGE_TYPE"
    message = "Unsupported image type."

    def __init__(self, content_type: str):
        self.message = f"Unsupported image type: {content_type}."

class ImageTooLarge(DomainException):
    status_code = status.HTTP_413_CONTENT_TOO_LARGE
    error_code = "IMAGE_TOO_LARGE"
    message = "Image is too large."

    def __init__(self, content_type: str, max_file_size: int):
        max_mb = round(max_file_size / (1024 * 1024), 1)
        self.message = f"Image is too large. For content type {content_type}, the maximum allowed size is {max_file_size} ({max_mb} MB)."

class PhotoProcessConflict(DomainException):
    status_code = status.HTTP_409_CONFLICT
    error_code = "PHOTO_PROCESS_CONFLICT"
    message = "Photo cannot be processed."


# -----------------------------------------------
# S3
# -----------------------------------------------

class S3PresignedUrlError(DomainException):
    status_code = status.HTTP_404_NOT_FOUND
    error_code = "PRESIGNED_URL_ERROR"
    message = "Presigned url error"


# -----------------------------------------------
# Images
# -----------------------------------------------

class ImageExtensionError(DomainException):
    status_code = status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
    error_code = "FILE_EXTENSION_ERROR"
    message = "Invalid file extension."

class ImageMimeError(DomainException):
    status_code = status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
    error_code = "FILE_MIME_ERROR"
    message = "Unsupported MIME type."

class ImageFileSizeError(DomainException):
    status_code = status.HTTP_413_CONTENT_TOO_LARGE
    error_code = "FILE_SIZE_ERROR"
    message = "File exceeds max size."

class ImageVerificationError(DomainException):
    status_code = status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
    error_code = "IMAGE_VERIFY_ERROR"
    message = "PIL cannot identify image."

class ImageDimensionsError(DomainException):
    status_code = status.HTTP_413_CONTENT_TOO_LARGE
    error_code = "IMAGE_DIMENSION_ERROR"
    message = "Image dimensions exceed limits."

class ImageLimitsError(DomainException):
    status_code = status.HTTP_404_NOT_FOUND
    error_code = "IMAGE_LIMITS_ERROR"
    message = f"No limits defined for MIME."

    
