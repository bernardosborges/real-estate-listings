from app.application.dto.user.user_output import UserOutput


class LoginUserOutput:

    def __init__(self, access_token: str, user: UserOutput):
        self.access_token = access_token
        self.user = user
