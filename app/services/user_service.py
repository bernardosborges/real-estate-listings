from sqlalchemy.orm import Session

from app.models.user_model import UserModel
from app.repositories.user_repository import get_user_by_email, add_user
from app.core.security import hash_password
from app.core.exceptions.domain_exception import EmailAlreadyRegistered

def register_user_service(db: Session, email: str, password: str) -> UserModel:
    if get_user_by_email(db, email):
        raise EmailAlreadyRegistered()
    
    user = UserModel(
        email=email,
        password_hash=hash_password(password),
        is_active=True,
        is_verified=False
    )
    
    add_user(db, user)
    db.commit()
    db.refresh(user)    
    return user