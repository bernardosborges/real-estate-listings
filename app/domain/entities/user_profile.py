from __future__ import annotations
from datetime import datetime, timezone
from typing import Dict, Any

from app.domain.value_objects.user_profile.user_profile_public_id import UserProfilePublicId
from app.domain.exceptions.domain_exception import FieldTooLong, AlreadyDeleted, CannotBeRestored
from app.domain.constants.user_profile_constants import (
    PROFILE_NAME_MAX_LENGHT,
    PROFILE_BIO_MAX_LENGHT,
    PROFILE_WORK_PHONE_MAX_LENGHT,
    PROFILE_WORK_CITY_MAX_LENGHT,
    PROFILE_LICENSE_NUMBER_MAX_LENGHT
)

class UserProfile:
    def __init__(
            self,
            id: int | None,
            public_id: UserProfilePublicId,
            user_id: int,
            name: str | None = None,
            bio: str | None = None,
            work_phone: str | None = None,
            work_city: str | None = None,
            license_number: str | None = None,
            profile_picture_url: str | None = None,
            background_image_url: str | None = None,
            preferences: Dict[str, Any] | None = None,
            deleted_at: datetime | None = None,
    ):
        
        self.id = id
        self.public_id = public_id
        self.user_id = user_id
        self.name = name
        self.bio = bio
        self.work_phone = work_phone
        self.work_city = work_city
        self.license_number = license_number
        self.profile_picture_url = profile_picture_url
        self.background_image_url = background_image_url
        self.preferences = preferences or {}
        self.deleted_at = deleted_at


# -----------------------------------------------
# LIFECYCLE
# -----------------------------------------------

    @property
    def is_deleted(self) -> bool:
        return self.deleted_at is not None

    def soft_delete(self) -> None:
        if self.is_deleted:
            raise AlreadyDeleted("user_profile")
        self.deleted_at = datetime.now(timezone.utc)

    def restore(self) -> None:
        if self.deleted_at is None:
            raise CannotBeRestored("user_profile")
        self.deleted_at = None


# -----------------------------------------------
# ?????
# -----------------------------------------------

    def update_basic_info(
            self,
            *,
            name: str | None = None,
            bio: str | None = None,
            work_phone: str | None = None,
            work_city: str | None = None,
            license_number: str | None = None
    ) -> None:
        if name is not None:
            if len(name) > PROFILE_NAME_MAX_LENGHT:
                raise FieldTooLong("name")
            self.name = name
        if bio is not None:
            if len(bio) > PROFILE_BIO_MAX_LENGHT:
                raise FieldTooLong("bio")
            self.bio = bio
        if work_phone is not None:
            if len(work_phone) > PROFILE_WORK_PHONE_MAX_LENGHT:
                raise FieldTooLong("work_phone")
            self.work_phone = work_phone
        if work_city is not None:
            if len(work_city) > PROFILE_WORK_CITY_MAX_LENGHT:
                raise FieldTooLong("work_city")
            self.work_city = work_city
        if license_number is not None:
            if len(license_number) > PROFILE_LICENSE_NUMBER_MAX_LENGHT:
                raise FieldTooLong("license_number")
            self.license_number = license_number

    def update_preferences(self, preferences: Dict[str, Any]) -> None:
        if not isinstance(preferences, dict):
            raise ValueError("Preferences must be a dictionary.")
        self.preferences = preferences
 