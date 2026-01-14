# from fastapi import Request, HTTPException
# from fastapi.responses import JSONResponse
# from sqlalchemy.exc import SQLAlchemyError



# async def http_exception_handler(request: Request, exc: HTTPException):
#     return JSONResponse(
#         status_code = exc.status_code,
#         content={"error": exc.detail, "path": str(request.url)}
#     )

# async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
#     return JSONResponse(
#         status_code=500,
#         content={"error": "Database error", "details": str(exc)}
#     )

# async def generic_exception_handler(request: Request, exc: Exception):
#     return JSONResponse(
#         status_code=500,
#         content={"error": "Internal server error", "details": str(exc)}
#     )


from fastapi import status

class DomainException(Exception):
    status_code: int = status.HTTP_400_BAD_REQUEST
    error_code: str = "DOMAIN_ERROR"
    message: str = "Domain error"

    def __init__(self, message: str | None = None):
        if message:
            self.message = message
        super().__init__(self.message)


# -----------------------------------------------
# AUTHENTICATION
# -----------------------------------------------

class InvalidCredentials(DomainException):
    status_code = status.HTTP_401_UNAUTHORIZED
    error_code = "INVALID_CREDENTIALS"
    message = "Invalid user credentials"


# -----------------------------------------------
# PROPERTY
# -----------------------------------------------

class PropertyForbidden(DomainException):
    status_code = status.HTTP_403_FORBIDDEN
    error_code = "PROPERTY_FORBIDDEN"
    message = "You do not have permission to access this property"

class PropertyNotFound(DomainException):
    status_code = status.HTTP_404_NOT_FOUND
    error_code = "PROPERTY_NOT_FOUND"
    message = "Property not found"


# -----------------------------------------------
# USER
# -----------------------------------------------

class EmailAlreadyRegistered(DomainException):
    status_code = status.HTTP_409_CONFLICT
    error_code = "EMAIL_ALREADY_REGISTERED"
    message = "Email already registered"

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
    status_code = status.HTTP_404_NOT_FOUND
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