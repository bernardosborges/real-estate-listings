from app.domain.entities.user_profile import UserProfile
from app.domain.repositories.user_profile_repository import UserProfileRepository
from app.domain.value_objects.user_profile.user_profile_public_id import UserProfilePublicId
from app.domain.exceptions.user_profile_exceptions import UserProfileNotFound




class FakeUserProfileRepository(UserProfileRepository):

    def __init__(self):
        self._profiles: list[UserProfile] = []
        self._next_id = 1


# -----------------------------------------------
# PERSISTENCE
# -----------------------------------------------

    def save(self, user_profile: UserProfile) -> UserProfile:
        if user_profile.id is None:
            user_profile.id = self._next_id
            self._next_id += 1

        self._profiles = [
            p for p in self._profiles if p.id != user_profile.id
        ]

        self._profiles.append(user_profile)
        return user_profile
    
    def refresh(self, user_profile: UserProfile) -> UserProfile | None: 
        return self.get_by_id(user_profile.id)
    
# -----------------------------------------------
# GETTERS
# -----------------------------------------------

    def get_by_id(self, id: int) -> UserProfile | None:
        for user_profile in self._profiles:
            if user_profile.id == id and user_profile.deleted_at is None:
                return user_profile
        return None


    def get_by_public_id(self, public_id: str) -> UserProfile | None:
        for user_profile in self._profiles:
            if user_profile.public_id == public_id and user_profile.deleted_at is None:
                return user_profile
        return None
    
    def get_deleted_by_public_id(self, public_id: str) -> UserProfile | None:
        for user_profile in self._profiles:
            if user_profile.public_id == public_id and user_profile.deleted_at is not None:
                return user_profile
        return None
    
    def get_by_user_id(self, user_id: int) -> UserProfile | None:
        for user_profile in self._profiles:
            if user_profile.user_id == user_id and user_profile.deleted_at is None:
                return user_profile
        return None
    
    def exists_by_public_id(self, public_id: UserProfilePublicId) -> bool:
        return any(p.public_id == public_id for p in self._profiles)

   
# -----------------------------------------------
# STATE CHANGES
# -----------------------------------------------
  
    def soft_delete(self, id: int) -> None:
        user_profile = self.get_by_id(id)
        if user_profile:
            user_profile.soft_delete()

    def restore(self, id: int) -> None:
        user_profile = self.get_by_id(id)
        if user_profile:
            user_profile.restore()