class ApplicationException(Exception):
    error_code: str = "APPLICATION_ERROR"
    message: str = "An application error ocurred."

    def __init__(self, message: str | None = None, **context):
        self.message = message or self.message
        self.context = context
        super().__init__(message or self.message)
