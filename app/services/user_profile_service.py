from sqlalchemy.orm import Session
import re

from app.models.user_profile_model import UserProfileModel, generate_handle
from app.models.user_model import UserModel
from app.repositories.user_profile_repository import UserProfileRepository
from app.application.services.auth_service import AuthService
from app.services.user_service import UserService
from app.core.exceptions.domain_exception import *

class UserProfileService:

# -----------------------------------------------
# CRUD - CREATE
# -----------------------------------------------

    @staticmethod
    def create(db: Session, user_id: int, public_id: str | None = None, current_user: UserModel | None = None) -> UserProfileModel:

        UserService.get_by_id(db, user_id)

        if current_user is not None:
            AuthService.ensure_owner_or_admin(user_id, current_user, "create", "user profile")
            
        db_user_profile = UserProfileService.get_by_user_id_or_none(db, user_id)
        if db_user_profile is not None:
            raise UserProfileAlreadyRegistered()

        if not public_id:
            public_id = generate_handle()
        UserProfileService._is_public_id_available_or_400(db, public_id)
        user_profile = UserProfileRepository.create(db, user_id, public_id)

        db.commit()
        db.refresh(user_profile) 

        return user_profile


# -----------------------------------------------
# CRUD - READ
# -----------------------------------------------

    @staticmethod
    def get_by_user_id_or_none(db: Session, user_id: int, include_deleted: bool = False) -> UserProfileModel | None:
        return UserProfileRepository.get_by_user_id(db, user_id, include_deleted)

    @staticmethod
    def get_by_id_or_404(db: Session, id: int, include_deleted: bool = False) -> UserProfileModel:
        db_user_profile = UserProfileRepository.get_by_id(db, id, include_deleted)
        if not db_user_profile:
            raise UserProfileNotFound()
        return db_user_profile
    
    @staticmethod
    def get_by_public_id_or_404(db: Session, public_id: str, include_deleted: bool = False) -> UserProfileModel:
        db_user_profile = UserProfileRepository.get_by_public_id(db, public_id, include_deleted)
        if not db_user_profile:
            raise UserProfileNotFound()
        return db_user_profile
    
    @staticmethod
    def get_by_user_id_or_404(db: Session, user_id: int, include_deleted: bool = False) -> UserProfileModel:
        db_user_profile = UserProfileRepository.get_by_user_id(db, user_id, include_deleted)
        if not db_user_profile:
            raise UserProfileNotFound()
        return db_user_profile
        

# -----------------------------------------------
# CRUD - UPDATE
# -----------------------------------------------

    @staticmethod
    def update(
        db: Session,
        public_id: str,
        current_user: UserModel | None = None,
        name: str | None = None,
        bio: str | None = None,
        work_phone: str | None = None,
        work_city: str | None = None,
        license_number: str | None = None,
        profile_picture_url: str | None = None,
        background_image_url: str | None = None,
        preferences: dict | None = None
    ) -> UserProfileModel:
        
        db_user_profile = UserProfileService.get_by_public_id_or_404(db, public_id)

        if current_user is not None:
            AuthService.ensure_owner_or_admin(db_user_profile.user_id, current_user, "edit", "user profile")

        update_data = {
            "name": name,
            "bio": bio,
            "work_phone": work_phone,
            "work_city": work_city,
            "license_number": license_number,
            "profile_picture_url": profile_picture_url,
            "background_image_url": background_image_url,
            "preferences": preferences
        }

        update_data = {k: v for k, v in update_data.items() if v is not None}

        updated_user_profile = UserProfileRepository.update(db, db_user_profile.id, **update_data)
        db.commit()
        db.refresh(updated_user_profile)

        return updated_user_profile


    @staticmethod
    def restore(db: Session, public_id: str, current_user: UserModel | None = None) -> UserProfileModel:
        db_user_profile = UserProfileService.get_by_public_id_or_404(db, public_id, include_deleted=True)

        if current_user is not None:
            AuthService.ensure_owner_or_admin(db_user_profile.user_id, current_user, "restore", "user profile")
        
        if db_user_profile.deleted_at is None:
            return db_user_profile
        
        restored_user_profile = UserProfileRepository.restore(db, db_user_profile.id)
        db.commit()
        db.refresh(restored_user_profile)

        return restored_user_profile


# -----------------------------------------------
# CRUD - DELETE
# -----------------------------------------------

    @staticmethod
    def soft_delete(db: Session, public_id: str, current_user: UserModel | None = None) -> UserProfileModel:
        db_user_profile = UserProfileService.get_by_public_id_or_404(db, public_id)

        if current_user is not None:
            AuthService.ensure_owner_or_admin(db_user_profile.user_id, current_user, "delete", "user profile")

        deleted = UserProfileRepository.soft_delete(db, db_user_profile.id)

        db.commit()
        db.refresh(deleted)

        return deleted


# -----------------------------------------------
# UTILS
# -----------------------------------------------
    
    @staticmethod
    def _is_public_id_valid(public_id: str) -> bool:
        pattern = re.compile(r'^[a-z0-9_.]{4,30}$')
        return bool(pattern.fullmatch(public_id))
        
    @staticmethod
    def _is_public_id_available_or_400(db: Session, public_id: str) -> bool:
        if not UserProfileService._is_public_id_valid(public_id):
            raise InvalidPublicId()
        if UserProfileRepository.get_by_public_id(db, public_id, include_deleted=True):
            raise PublicIdNotAvailable()
        return True
