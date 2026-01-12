from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.core.exceptions.domain_exception import EmailAlreadyRegistered
from app.models.user_model import UserModel


# -----------------------------------------------
# CRUD - CREATE
# -----------------------------------------------

def add_user(db: Session, user: UserModel) -> UserModel:
    try:
        db.add(user)
        db.flush()
        return user
    except IntegrityError:
        db.rollback()
        raise EmailAlreadyRegistered()


# -----------------------------------------------
# CRUD - READ
# -----------------------------------------------

def get_user_by_email(db: Session, email: str) -> UserModel | None:
    return db.query(UserModel).filter(UserModel.email == email).first()

def get_user_by_id(db: Session, user_id: str) -> UserModel | None:
    return db.query(UserModel).filter(UserModel.id == user_id).first()


# -----------------------------------------------
# CRUD - UPDATE
# -----------------------------------------------

# -----------------------------------------------
# CRUD - DELETE
# -----------------------------------------------