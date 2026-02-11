from abc import ABC, abstractmethod
from app.domain.entities.user_profile import UserProfile
from app.domain.value_objects.user_profile.user_profile_public_id import UserProfilePublicId

class UserProfileRepository(ABC):

    @abstractmethod
    def refresh(self, profile: UserProfile) -> UserProfile:
        pass

    @abstractmethod
    def save(self, profile: UserProfile) -> UserProfile:
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> UserProfile | None:
        pass

    @abstractmethod
    def get_by_public_id(self, public_id: str) -> UserProfile | None:
        pass

    @abstractmethod
    def get_deleted_by_public_id(self, public_id: str) -> UserProfile | None:
        pass

    @abstractmethod
    def get_by_user_id(self, user_id: int) -> UserProfile | None:
        pass

    @abstractmethod
    def exists_by_public_id(self, public_id: UserProfilePublicId) -> bool:
        pass

  