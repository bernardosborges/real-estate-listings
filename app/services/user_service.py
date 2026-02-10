from sqlalchemy.orm import Session

from app.models.user_model import UserModel
from app.repositories.user_repository_SQLAlchemy import UserRepository
from app.core.security import hash_password
from app.core.exceptions.domain_exception import EmailAlreadyRegistered, UserNotFound

class UserService:

# -----------------------------------------------
# CRUD - CREATE
# -----------------------------------------------

    @staticmethod
    def register_user_service(db: Session, email: str, password: str) -> UserModel:
        if UserRepository.get_by_email(db, email):
            raise EmailAlreadyRegistered()
        
        user = UserModel(
            email=email,
            password_hash=hash_password(password),
            is_active=True,
            is_verified=False
        )
        
        UserRepository.add_user(db, user)
        db.commit()
        db.refresh(user)    
        return user


# -----------------------------------------------
# CRUD - READ
# -----------------------------------------------

    @staticmethod
    def get_by_id(db: Session, id: int) -> UserModel:
        db_user = UserRepository.get_by_id(db, id)
        if not db_user:
            raise UserNotFound(f"User id: {id} not found")
        return db_user
    
    @staticmethod
    def get_by_id_or_none(db: Session, id: int) -> UserModel | None:
        return UserRepository.get_by_id(db, id)


# -----------------------------------------------
# CRUD - UPDATE
# -----------------------------------------------

# -----------------------------------------------
# CRUD - DELETE
# -----------------------------------------------