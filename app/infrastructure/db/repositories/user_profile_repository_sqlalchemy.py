from sqlalchemy import select, exists
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.domain.entities.user_profile import UserProfile
from app.domain.repositories.user_profile_repository import UserProfileRepository
from app.domain.value_objects.user_profile.user_profile_public_id import (
    UserProfilePublicId,
)
from app.infrastructure.db.models.user_profile_model import UserProfileModel
from app.infrastructure.db.mappers.user_profile_mapper import UserProfileMapper
from app.domain.exceptions.user_profile_exceptions import UserProfileNotFound


class UserProfileRepositorySQLAlchemy(UserProfileRepository):

    # -----------------------------------------------
    # INIT
    # -----------------------------------------------

    def __init__(self, db: Session):
        self.db = db

    # -----------------------------------------------
    # METHODS
    # -----------------------------------------------

    def commit(self):
        self.db.commit()

    def refresh(self, user_profile: UserProfile) -> UserProfile:
        model = self.db.get(UserProfile, user_profile.id)
        if not model or model.deleted_at:
            return None
        self.db.refresh(model)

        refreshed_profile = UserProfileMapper.to_entity(model)
        return UserProfileMapper.update_entity(user_profile, refreshed_profile)

    def save(self, profile: UserProfile) -> UserProfile:
        if profile.id is None:
            model = UserProfileMapper.to_model(profile)
            self.db.add(model)
        else:
            model = self.db.get(UserProfileModel, profile.id)
            if not model or model.deleted_at is not None:
                raise UserProfileNotFound(
                    f"User profile not found or deleted: public id {profile.public_id}."
                )
            UserProfileMapper.update_model(model, profile)

        try:
            self.db.flush()
        except IntegrityError as exc:
            self.db.rollback()
            raise exc

        return UserProfileMapper.to_entity(model)

    def get_by_id(self, id: int) -> UserProfile | None:
        model = self.db.get(UserProfileModel, id)
        if not model or model.deleted_at is not None:
            return None
        return UserProfileMapper.to_entity(model)

    def get_by_public_id(self, public_id: str) -> UserProfile | None:
        model = (
            self.db.query(UserProfileModel)
            .filter(
                UserProfileModel.public_id == public_id,
                UserProfileModel.deleted_at.is_(None),
            )
            .one_or_none()
        )

        return UserProfileMapper.to_entity(model) if model else None

    def get_deleted_by_public_id(self, public_id: str) -> UserProfile | None:
        model = (
            self.db.query(UserProfileModel)
            .filter(
                UserProfileModel.public_id == public_id,
                UserProfileModel.deleted_at.isnot(None),
            )
            .one_or_none()
        )

        return UserProfileMapper.to_entity(model) if model else None

    def get_by_user_id(self, user_id: int) -> UserProfile | None:
        model = (
            self.db.query(UserProfileModel)
            .filter(
                UserProfileModel.user_id == user_id,
                UserProfileModel.deleted_at.is_(None),
            )
            .one_or_none()
        )

        return UserProfileMapper.to_entity(model) if model else None

    def exists_by_public_id(self, public_id: UserProfilePublicId) -> bool:
        stmt = select(exists().where(UserProfileModel.public_id == public_id))
        return self.db.execute(stmt).scalar()


# # -----------------------------------------------
# # CRUD - CREATE
# # -----------------------------------------------

#     @staticmethod
#     def create(db: Session, user_id: int, public_id: str) -> UserProfileModel:

#         db_user_profile = UserProfileModel(user_id=user_id, public_id=public_id)

#         try:
#             db.add(db_user_profile)
#             db.flush()
#             return db_user_profile
#         except IntegrityError:
#             db.rollback()
#             raise


# # -----------------------------------------------
# # CRUD - READ
# # -----------------------------------------------

#     @staticmethod
#     def get_by_id(db: Session, id: int, include_deleted: bool = False) -> UserProfileModel | None:
#         query = db.query(UserProfileModel).filter(UserProfileModel.id == id)
#         if not include_deleted:
#             query = query.filter(UserProfileModel.deleted_at.is_(None))

#         return query.first()

#     @staticmethod
#     def get_by_public_id(db: Session, public_id: str, include_deleted: bool = False) -> UserProfileModel | None:
#         query = db.query(UserProfileModel).filter(UserProfileModel.public_id == public_id)
#         if not include_deleted:
#             query = query.filter(UserProfileModel.deleted_at.is_(None))

#         return query.first()

#     @staticmethod
#     def get_by_user_id(db: Session, user_id: int, include_deleted: bool = False) -> UserProfileModel | None:
#         query = db.query(UserProfileModel).filter(UserProfileModel.user_id == user_id)
#         if not include_deleted:
#             query = query.filter(UserProfileModel.deleted_at.is_(None))

#         return query.first()


# # -----------------------------------------------
# # CRUD - UPDATE
# # -----------------------------------------------

#     @staticmethod
#     def update(db: Session, id: int, **kwargs) -> UserProfileModel | None:
#         db_user_profile = UserProfileRepository.get_by_id(db, id)
#         if not db_user_profile:
#             return None

#         for key, value in kwargs.items():
#             setattr(db_user_profile, key, value)
#         return db_user_profile

#     @staticmethod
#     def restore(db: Session, id: int) -> UserProfileModel | None:
#         db_user_profile = UserProfileRepository.get_by_id(db, id, include_deleted=True)
#         if not db_user_profile:
#             return None

#         db_user_profile.deleted_at = None

#         return db_user_profile


# # -----------------------------------------------
# # CRUD - DELETE
# # -----------------------------------------------

#     @staticmethod
#     def soft_delete(db: Session, id: int) -> UserProfileModel | None:
#         return UserProfileRepository._delete(db, id, hard=False)

#     @staticmethod
#     def hard_delete(db: Session, id: int) -> UserProfileModel | None:
#         return UserProfileRepository._delete(db, id, hard=True)

#     @staticmethod
#     def _delete(db: Session, id: int, hard: bool = False) -> UserProfileModel | None:
#         db_user_profile = UserProfileRepository.get_by_id(db, id)
#         if not db_user_profile:
#             return None

#         if hard:
#             db.delete(db_user_profile)
#         else:
#             db_user_profile.deleted_at = datetime.now(timezone.utc)

#         return db_user_profile
