from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.domain.entities.user_profile import UserProfile


class User:
    def __init__(
        self,
        *,
        id: int | None,
        email: str,
        password_hash: str,
        is_active: bool,
        is_verified: bool = False,
        is_superuser: bool = False,
        profile: UserProfile | None = None,
    ):
        self.id = id
        self.email = email
        self.password_hash = password_hash
        self.is_active = is_active
        self.is_verified = is_verified
        self.is_superuser = is_superuser
        self.profile = profile

    def activate(self):
        self.is_active = True

    def deactivate(self):
        self.is_active = False

    def attach_profile(self, profile: UserProfile) -> None:
        self.profile = profile
