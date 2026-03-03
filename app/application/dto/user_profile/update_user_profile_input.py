class UpdateUserProfileInput:

    def __init__(
        self,
        name: str | None = None,
        bio: str | None = None,
        work_phone: str | None = None,
        work_city: str | None = None,
        license_number: str | None = None,
        profile_picture_url: str | None = None,
        background_image_url: str | None = None,
        preferences: dict | None = None,
    ):

        self.name = name
        self.bio = bio
        self.work_phone = work_phone
        self.work_city = work_city
        self.license_number = license_number
        self.profile_picture_url = profile_picture_url
        self.background_image_url = background_image_url
        self.preferences = preferences
