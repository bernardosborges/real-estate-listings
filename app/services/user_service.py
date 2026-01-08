from sqlalchemy.orm import Session
from app.models.user_model import UserModel
from app. repositories.user_repository import get_user_by_email, add_user
from app.services.auth_service import hash_password, verify_password, create_access_token

def register_user_service(db: Session, email: str, password: str) -> UserModel:
    if get_user_by_email(db, email):
        raise ValueError("Email already registered")
    
    user = UserModel(
        email=email,
        password_hash=hash_password(password),
        is_active=True,
        is_verified=False
    )
    
    try:
        add_user(db, user)
        db.commit()
        db.refresh(user)
    except Exception as e:
        db.rollback()
        raise e
    
    return user

def login_user_service(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.password_hash):
        return None
    
    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}