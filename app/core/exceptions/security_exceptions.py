class InvalidToken(Exception):
    error_code: str = "INVALID_TOKEN"
    message: str = "Invalid token."
