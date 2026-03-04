from fastapi import Security, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError

from app.core.security import decode_access_token
from app.core.database import get_db
from app.core.config import settings
from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository
from app.infrastructure.db.repositories.user_repository_sqlalchemy import (
    UserRepositorySQLAlchemy,
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_PREFIX}/auth/login")

# Dependency


def get_current_user_optional() -> User | None:
    try:
        return get_current_user()
    except (HTTPException, JWTError):
        return None


def get_current_user(token: str = Security(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    try:
        payload = decode_access_token(token)
        if payload is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

        user_id = int(payload.get("sub"))
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")

        user_repository: UserRepository = UserRepositorySQLAlchemy(db)
        user = user_repository.get_by_id(int(user_id))
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

        return user

    except JWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        ) from exc


def superuser_required(current_user: User = Security(get_current_user)) -> User:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource",
        )
    return current_user
