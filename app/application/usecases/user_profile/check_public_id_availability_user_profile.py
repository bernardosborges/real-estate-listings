from app.domain.repositories.user_profile_repository import UserProfileRepository
from app.domain.value_objects.user_profile.user_profile_public_id import UserProfilePublicId



class CheckProfilePublicIdAvailabilityUseCase:

    def __init__(self, repository: UserProfileRepository):
        self.repository = repository

    
    def execute(self, raw_public_id: str) -> bool:
        public_id = UserProfilePublicId.from_raw(raw_public_id)

        return not self.repository.exists_by_public_id(public_id)