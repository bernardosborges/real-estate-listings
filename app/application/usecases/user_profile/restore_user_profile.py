from app.domain.repositories.user_profile_repository import UserProfileRepository
from app.application.dto.user_profile.user_profile_output import UserProfileOutput
from app.core.exceptions.domain_exception import UserProfileNotFound

class RestoreUserProfileUseCase:

    def __init__(self, user_profile_repository: UserProfileRepository):
        self.user_profile_repository = user_profile_repository

    def execute(self, public_id: str) -> UserProfileOutput:
        profile = self.user_profile_repository.get_deleted_by_public_id(public_id)
        if not profile:
            raise UserProfileNotFound(f"Deleted user profile not found: {public_id}")
        
        # Business rules
        profile.restore()

        # Persistence
        self.user_profile_repository.save(profile)

        return UserProfileOutput.from_entity(profile)
        