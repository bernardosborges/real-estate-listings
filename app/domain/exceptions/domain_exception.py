
class DomainException(Exception):
    error_code: str = "DOMAIN_ERROR"
    message: str = "A domain error ocurred."

    def __init__(self, message: str | None = None, **context):
        self.message = message or self.message
        self.context = context
        super().__init__(message or self.message)


class AlreadyDeactivated(DomainException):
    error_code = "RESOURCE_ALREADY_DEACTIVATED"
    message = "This resource is already deactivated."

    def __init__(self, entity: str):
        super().__init__(
            message = f"This {entity} is already deactivated.",
            entity = entity
        )


class AlreadyActive(DomainException):
    error_code = "RESOURCE_ALREADY_ACTIVE"
    message = "This resource is already active."

    def __init__(self, entity: str):
        super().__init__(
            message = f"This {entity} is already active.",
            entity = entity
        )


class CannotBeRestored(DomainException):
    error_code = "RESOURCE_CANNOT_BE_RESTORED"
    message = "Cannot restore a resource that has not been deleted."

    def __init__(self, entity: str):
        super().__init__(
            message = f"Cannot restore a {entity} that has not been deleted.",
            entity = entity
        )


class AlreadyDeleted(DomainException):
    error_code = "RESOURCE_ALREADY_DELETED"
    message = "This resource was already deleted."

    def __init__(self, entity: str):
        super().__init__(
            message = f"This {entity} is already deleted.",
            entity = entity
        )


class FieldTooLong(DomainException):
    error_code = "FIELD_TOO_LONG"
    message = "The field exceeds the maximum allowed length."

    def __init__(self, field: str):
        super().__init__(
            message = f"The field {field} exceeds the maximum allowed length.",
            field = field
        )