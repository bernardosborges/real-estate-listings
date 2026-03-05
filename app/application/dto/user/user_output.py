from __future__ import annotations
from app.application.dto.user_profile.user_profile_output import UserProfileOutput


class UserOutput:
    def __init__(self, id: int, email: str, is_superuser: bool, profile: UserProfileOutput | None):
        self.id = id
        self.email = email
        self.is_superuser = is_superuser
        self.profile = profile

    @classmethod
    def from_entity(cls, user):
        return cls(
            id=user.id,
            email=user.email,
            is_superuser=user.is_superuser,
            profile=(UserProfileOutput.from_entity(user.profile) if user.profile else None),
        )
