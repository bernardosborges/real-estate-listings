from datetime import datetime, timezone, timedelta
from jose import jwt, JWTError

from app.core.config import settings
from app.core.exceptions.security_exceptions import InvalidToken
from app.application.services.token_service import TokenService


class JWTTokenService(TokenService):

    def generate(self, subject: str) -> dict:

        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        payload = {"sub": subject, "exp": expire}

        access_token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return access_token

    def decode(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            return payload
        except JWTError as exc:
            raise InvalidToken() from exc
