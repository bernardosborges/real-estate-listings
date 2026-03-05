from sqlalchemy import select, exists
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository
from app.domain.value_objects.user.user_email import UserEmail
from app.infrastructure.db.models.user_model import UserModel
from app.infrastructure.db.mappers.user_mapper import UserMapper
from app.domain.exceptions.user_exceptions import UserNotFound


class UserRepositorySQLAlchemy(UserRepository):

    # -----------------------------------------------
    # INIT
    # -----------------------------------------------

    def __init__(self, db: Session):
        self.db = db

    def commit(self):
        self.db.commit()

    def refresh(self, user: User) -> User:
        model = self.db.get(UserModel, user.id)
        if not model or model.deleted_at:
            return None
        self.db.refresh(model)

        refreshed_user = UserMapper.to_entity(model)
        return UserMapper.update_entity(user, refreshed_user)

    # -----------------------------------------------
    # CRUD - CREATE/UPDATE
    # -----------------------------------------------

    def save(self, user: User):
        if user.id is None:
            model = UserMapper.to_model(user)
            self.db.add(model)
        else:
            model = self.db.get(UserModel, user.id)
            if not model or model.deleted_at is not None:
                raise UserNotFound("User not found or deleted.")
            UserMapper.update_model(model, user)

        try:
            self.db.flush()
            user.id = model.id
        except IntegrityError as exc:
            self.db.rollback()
            raise exc  # Tech exception

    # -----------------------------------------------
    # CRUD - READ
    # -----------------------------------------------

    def get_by_id(self, user_id: int) -> User | None:
        model = self.db.get(UserModel, user_id)
        return UserMapper.to_entity(model)

    def get_by_email(self, email: str) -> User | None:
        model = self.db.query(UserModel).filter(UserModel.email == email).first()
        return UserMapper.to_entity(model)

    def exists_by_email(self, email: UserEmail) -> bool:
        stmt = select(exists().where(UserModel.email == email))
        return self.db.execute(stmt).scalar()


# -----------------------------------------------
# CRUD - CREATE
# -----------------------------------------------

# @staticmethod
# def add_user(db: Session, user: UserModel) -> UserModel:
#     try:
#         db.add(user)
#         db.flush()
#         return user
#     except IntegrityError:
#         db.rollback()
#         raise EmailAlreadyRegistered()


# -----------------------------------------------
# CRUD - READ
# -----------------------------------------------

# @staticmethod
# def get_by_email(db: Session, email: str) -> UserModel | None:
#     return db.query(UserModel).filter(UserModel.email == email).first()

# @staticmethod
# def get_by_id(db: Session, user_id: str) -> UserModel | None:
#     return db.query(UserModel).filter(UserModel.id == user_id).first()


# -----------------------------------------------
# CRUD - UPDATE
# -----------------------------------------------

# -----------------------------------------------
# CRUD - DELETE
# -----------------------------------------------
