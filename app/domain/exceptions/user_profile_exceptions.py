from app.domain.exceptions.domain_exception import DomainException

# -----------------------------------------------
# USER PROFILE
# -----------------------------------------------


class UserProfileNotFound(DomainException):
    error_code = "USER_PROFILE_NOT_FOUND"
    message = "User profile not found."

    def __init__(self, public_id: str):
        super().__init__(message=f"User profile not found: public id '{public_id}'.", public_id=public_id)


class InvalidProfileId(DomainException):
    error_code = "INVALID_USER_PROFILE_ID"
    message = "Invalid profile id."

    def __init__(self):
        super().__init__(message="Invalid user profile id.")


class UserProfileAlreadyRegistered(DomainException):
    error_code = "USER_PROFILE_ALREADY_REGISTERED"
    message = "User profile already registered."

    def __init__(self, user_id: int):
        super().__init__(message=f"User profile already registered for user: '{user_id}'.", user_id=user_id)


class InvalidProfilePublicId(DomainException):
    error_code = "INVALID_PROFILE_PUBLIC_ID"
    message = "Invalid profile public id."

    def __init__(self, public_id: str):
        super().__init__(message=f"Invalid profile public id: '{public_id}'.", public_id=public_id)


class ProfilePublicIdNotAvailable(DomainException):
    error_code = "PROFILE_PUBLIC_ID_NOT_AVAILABLE"
    message = "Profile public id not available."

    def __init__(self, public_id: str):
        super().__init__(message=f"Profile public id not available: '{public_id}'.", public_id=public_id)


class InvalidWorkPhone(DomainException):
    error_code = "INVALID_WORK_PHONE"
    message = "Invalid work phone."

    def __init__(self, work_phone: str):
        super().__init__(message=f"Invalid work phone: '{work_phone}'.", work_phone=work_phone)
