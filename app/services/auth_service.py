from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import verify_password, create_access_token
from app.repositories.user_repository import get_user_by_email
from app.models.user_model import UserModel

def authenticate_user_service(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user credentials")
    return user

def generate_token_for_user_service(user: UserModel):
    access_token = create_access_token(data={"sub":user.id})
    return {"access_token": access_token, "token_type": "bearer"}