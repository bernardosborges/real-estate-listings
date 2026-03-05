from app.domain.entities.user_profile import UserProfile
from app.infrastructure.db.models.user_profile_model import UserProfileModel


class UserProfileMapper:

    @staticmethod
    def to_entity(model: UserProfileModel) -> UserProfile:
        if model is None:
            return None

        return UserProfile(
            id=model.id,
            public_id=model.public_id,
            user_id=model.user_id,
            name=model.name,
            bio=model.bio,
            work_phone=model.work_phone,
            work_city=model.work_city,
            license_number=model.license_number,
            profile_picture_url=model.profile_picture_url,
            background_image_url=model.background_image_url,
            preferences=model.preferences,
            deleted_at=model.deleted_at,
        )

    @staticmethod
    def to_model(entity: UserProfile) -> UserProfileModel:
        return UserProfileModel(
            id=entity.id,
            public_id=entity.public_id,
            user_id=entity.user_id,
            name=entity.name,
            bio=entity.bio,
            work_phone=entity.work_phone,
            work_city=entity.work_city,
            license_number=entity.license_number,
            profile_picture_url=entity.profile_picture_url,
            background_image_url=entity.background_image_url,
            preferences=entity.preferences,
            deleted_at=entity.deleted_at,
        )

    @staticmethod
    def update_model(model: UserProfileModel, entity: UserProfile):
        model.user_id = entity.user_id
        model.name = entity.name
        model.bio = entity.bio
        model.work_phone = entity.work_phone
        model.work_city = entity.work_city
        model.license_number = entity.license_number
        model.profile_picture_url = entity.profile_picture_url
        model.background_image_url = entity.background_image_url
        model.preferences = entity.preferences
        model.deleted_at = entity.deleted_at

    @staticmethod
    def update_entity(target: UserProfile, source: UserProfile):
        target.name = source.name
        target.bio = source.bio
        target.work_phone = source.work_phone
        target.work_city = source.work_city
        target.license_number = source.license_number
        target.profile_picture_url = source.profile_picture_url
        target.background_image_url = source.background_image_url
        target.preferences = source.preferences
        target.deleted_at = source.deleted_at
