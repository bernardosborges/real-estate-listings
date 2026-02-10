
class APIException(Exception):
    error_code: str = "API_ERROR"
    message: str = "An API error ocurred."

    def __init__(self, message: str | None = None, **context):
        self.message = message or self.message
        self.context = context
        super().__init__(message or self.message)