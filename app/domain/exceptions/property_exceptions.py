from app.domain.exceptions.domain_exception import DomainException

# -----------------------------------------------
# USER PROFILE
# -----------------------------------------------

class InvalidPropertyPublicId(DomainException):
    error_code = "INVALID_PROPERTY_PUBLIC_ID"
    message = "Invalid property public id."

    def __init__(self, public_id: str):
        super().__init__(
            message = f"Invalid property public id: '{public_id}'.",
            public_id = public_id
        )

class PropertyForbidden(DomainException):
    error_code = "PROPERTY_FORBIDDEN"
    message = "You do not have permission to access this property"

class PropertyNotFound(DomainException):
    error_code = "PROPERTY_NOT_FOUND"
    message = "Property not found"

class PropertyAlreadyDeactivated(DomainException):
    error_code = "PROPERTY_ALREADY_DEACTIVATED"
    message = "This property is already deactivated."

class PropertyAlreadyActive(DomainException):
    error_code = "PROPERTY_ALREADY_ACTIVE"
    message = "This property is already active."

class PropertyCannotBeRestored(DomainException):
    error_code = "PROPERTY_CANNOT_BE_RESTORED"
    message = "Cannot restore a property that has not been deleted."

class PropertyAlreadyDeleted(DomainException):
    error_code = "PROPERTY_ALREADY_DELETED"
    message = "This property was already deleted."


# -----------------------------------------------
# PROPERTY
# -----------------------------------------------

class InvalidPrice(DomainException):
    error_code = "INVALID_PRICE"
    message = "Invalid price."

class InvalidPrivateArea(DomainException):
    error_code = "INVALID_PRIVATE_AREA"
    message = "Invalid private area."
