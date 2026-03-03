from app.domain.repositories.user_profile_repository import UserProfileRepository
from app.domain.exceptions.user_profile_exceptions import UserProfileNotFound
from app.application.dto.user_profile.update_user_profile_input import UpdateUserProfileInput
from app.application.dto.user_profile.user_profile_output import UserProfileOutput

class UpdateUserProfileUseCase:

    def __init__(self, user_profile_repository: UserProfileRepository):
        self.user_profile_repository = user_profile_repository

    def execute(self, public_id: str, data: UpdateUserProfileInput) -> UserProfileOutput:
        profile = self.user_profile_repository.get_by_public_id(public_id)
        if not profile:
            raise UserProfileNotFound(f"User profile not found or deleted: {public_id}")

        # Business rules
        for field, value in data.__dict__.items():
            if value is not None:
                setattr(profile, field, value)

        # Persistence
        self.user_profile_repository.save(profile)

        return UserProfileOutput.from_entity(profile)
