from app.domain.exceptions.domain_exception import DomainException

# -----------------------------------------------
# USER
# -----------------------------------------------

class InvalidEmail(DomainException):
    error_code = "INVALID_EMAIL"
    message = "Invalid email."

    def __init__(self, email: str):
        super().__init__(
            message = f"Email '{email}' is invalid.",
            email = email
        )


class EmailAlreadyRegistered(DomainException):
    error_code = "EMAIL_ALREADY_REGISTERED"
    message = "Email already registered."

    def __init__(self, email: str):
        super().__init__(
            message = f"Email '{email}' already registered.",
            email = email
        )


class UserNotFound(DomainException):
    error_code = "USER_NOT_FOUND"
    message = "User not found."

    def __init__(self, public_id: str):
        super().__init__(
            message = f"User not found with public id: '{public_id}'.",
            public_id = public_id
        )


class InvalidUserPublicId(DomainException):
    error_code = "INVALID_USER_PUBLIC_ID"
    message = "Public id must be 4-30 characteres and contain only lowercase letters, numbers, '_' or '.'."

    def __init__(self, public_id: str):
        super().__init__(
            message = f"Invalid public id '{public_id}'. Public id must be 4-30 characteres and contain only lowercase letters, numbers, '_' or '.'.",
            public_id = public_id
        )