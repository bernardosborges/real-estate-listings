from app.application.dto.user.login_user_input import LoginUserInput
from app.application.dto.user.login_user_output import LoginUserOutput
from app.application.dto.user.user_output import UserOutput
from app.application.services.password_hasher_service import PasswordHasher
from app.application.services.token_service import TokenService
from app.domain.repositories.user_repository import UserRepository
from app.domain.value_objects.user.user_email import UserEmail
from app.domain.exceptions.auth_exceptions import InvalidCredentials


class LoginUserUseCase:

    def __init__(self, user_repository: UserRepository, token_service: TokenService, password_hasher: PasswordHasher):
        self.user_repository = user_repository
        self.password_hasher = password_hasher
        self.token_service = token_service

    def execute(self, data: LoginUserInput) -> LoginUserOutput:

        # Validate & check email and password
        email = UserEmail.from_raw(data.email)
        db_user = self.user_repository.get_by_email(email)
        if not db_user:
            raise InvalidCredentials()

        is_authenticated = self.password_hasher.verify(data.password, db_user.password_hash)
        if not is_authenticated:
            raise InvalidCredentials()

        # if not db_user.is_active:
        #     raise USER NÃO TEM ATIVO OU NÃO APENAS PROFILE

        access_token = self.token_service.generate(subject=str(db_user.id))

        return LoginUserOutput(access_token=access_token, user=UserOutput.from_entity(db_user))
