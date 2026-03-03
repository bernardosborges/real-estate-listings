from app.domain.exceptions.domain_exception import DomainException

class InvalidCredentials(DomainException):
    error_code = "INVALID_CREDENTIALS"
    message = "Invalid user credentials."

class ForbiddenAction(DomainException):
    error_code = "PERMISSION_DENIED"
    message = "You are not allowed to perform this action."

    def __init__(self, action: str, resource: str):
        super().__init__(
            message = f"You are not allowed to {action} this {resource}.",
            action = action,
            resource = resource
        )
