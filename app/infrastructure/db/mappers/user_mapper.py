from app.domain.entities.user import User
from app.infrastructure.db.models.user_model import UserModel
from app.infrastructure.db.mappers.user_profile_mapper import UserProfileMapper


class UserMapper:

    @staticmethod
    def to_entity(model: UserModel) -> User:
        if model is None:
            return None

        profile_entity = None
        if model.user_profile:
            profile_entity = UserProfileMapper.to_entity(model.user_profile)

        return User(
            id=model.id,
            email=model.email,
            password_hash=model.password_hash,
            is_active=model.is_active,
            is_verified=model.is_verified,
            is_superuser=model.is_superuser,
            profile=profile_entity,
        )

    @staticmethod
    def to_model(entity: User) -> UserModel:
        model = UserModel(
            id=entity.id,
            email=entity.email,
            password_hash=entity.password_hash,
            is_active=entity.is_active,
            is_verified=entity.is_verified,
            is_superuser=entity.is_superuser,
        )

        if entity.profile:
            model.user_profile = UserProfileMapper.to_model(entity.profile)

        return model

    @staticmethod
    def update_model(model: UserModel, entity: User):
        model.password_hash = entity.password_hash
        model.is_active = entity.is_active
        model.is_verified = entity.is_verified
        model.is_superuser = entity.is_superuser
        if entity.profile:
            if model.user_profile:
                UserProfileMapper.update_model(model.user_profile, entity.profile)
            else:
                model.user_profile = UserProfileMapper.to_model(entity.profile)

    @staticmethod
    def update_entity(target: User, source: User) -> User:
        target.password_hash = source.password_hash
        target.is_active = source.is_active
        target.is_verified = source.is_verified
        target.is_superuser = source.is_superuser
        target.profile = source.profile
        return target
