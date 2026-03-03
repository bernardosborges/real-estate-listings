from app.domain.entities.user_profile import UserProfile
from app.domain.repositories.user_profile_repository import UserProfileRepository
from app.core.utils.id_generator import IDGenerator


class CreateUserProfileUseCase:
    """
    Use case responsible for creating a UserProfile associated with a User.
    Does not perform a commit, because it is always called with de User creation flow,
    enrusing the whole transaction remains atomic.
    """

    def __init__(self, repository: UserProfileRepository):
        self.repository = repository

    def execute(self, user_id: int) -> UserProfile:
        public_id = IDGenerator.generate_profile_public_id()

        # Create the User Profile entity
        profile = UserProfile(id=None, public_id=public_id, user_id=user_id)

        # Save the profile (internal flush), without comitting
        self.repository.save(profile)

        # Commit will be handled in the CreateUserUseCase to maintain atomicity
        return profile
