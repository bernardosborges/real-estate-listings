from datetime import datetime

class UserProfileOutput:

    def __init__(
            self,
            public_id: str,
            name: str | None,
            bio: str | None,
            work_phone: str | None,
            work_city: str | None,
            license_number: str | None,
            profile_picture_url: str | None,
            background_image_url: str | None,
            preferences: dict,
            deleted_at: datetime | None
    ):
        
        self.public_id = public_id
        self.name = name
        self.bio = bio
        self.work_phone = work_phone
        self.work_city = work_city
        self.license_number = license_number
        self.profile_picture_url = profile_picture_url
        self.background_image_url = background_image_url
        self.preferences = preferences
        self.deleted_at = deleted_at

    @classmethod
    def from_entity(cls, profile):
        return cls(
            public_id = profile.public_id,
            name = profile.name,
            bio = profile.bio,
            work_phone = profile.work_phone,
            work_city = profile.work_city,
            license_number = profile.license_number,
            profile_picture_url = profile.profile_picture_url,
            background_image_url = profile.background_image_url,
            preferences = profile.preferences,
            deleted_at = profile.deleted_at,
        )