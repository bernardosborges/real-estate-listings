from __future__ import annotations

from app.core.utils.id_generator import IDGenerator
from app.domain.entities.user_profile import UserProfile
from app.domain.exceptions.user_profile_exceptions import InvalidProfilePublicId
from app.domain.value_objects.user_profile.user_profile_public_id import UserProfilePublicId
from app.domain.constants.user_profile_constants import PROFILE_PUBLIC_ID_SIZE


class UserProfileFactory:

    @classmethod
    def create_for_user(
        cls,
        *,
        user_id: int,
        public_id: str | None = None
    ) -> UserProfile:
        
        if public_id is None:
            public_id = IDGenerator.generate_profile_public_id(PROFILE_PUBLIC_ID_SIZE)

        public_id = UserProfilePublicId.from_raw(public_id)

        return UserProfile(
            id = None,
            public_id = public_id,
            user_id = user_id,
            name = None,
            bio = None,
            work_phone = None,
            work_city = None,
            license_number = None,
            profile_picture_url = None,
            background_image_url = None,
            preferences = {},
            deleted_at = None,
        )
    


    