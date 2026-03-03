from app.domain.entities.user import User
from app.domain.factories.user_factory import UserFactory
from app.domain.factories.user_profile_factory import UserProfileFactory
from app.domain.repositories.user_repository import UserRepository
from app.domain.repositories.user_profile_repository import UserProfileRepository
from app.domain.exceptions.user_exceptions import EmailAlreadyRegistered
from app.domain.exceptions.user_profile_exceptions import ProfilePublicIdNotAvailable
from app.domain.exceptions.auth_exceptions import ForbiddenAction
from app.domain.value_objects.user.user_email import UserEmail
from app.domain.value_objects.user_profile.user_profile_public_id import UserProfilePublicId
from app.application.dto.user.user_output import UserOutput
from app.application.dto.user.create_user_input import CreateUserInput
from app.application.services.password_hasher_service import PasswordHasher


class RegisterUserUseCase:

    """
    Use case responsible for creating a new User along with its associated UserProfile.
    """

    def __init__(
            self,
            user_repository: UserRepository,
            profile_repository: UserProfileRepository,
            password_hasher: PasswordHasher
        ):

        self.user_repository = user_repository
        self.profile_repository = profile_repository
        self.password_hasher = password_hasher


    def execute(self, data: CreateUserInput, current_user: User | None = None) -> UserOutput:

        # Validate & check profile public id
        public_id = UserProfilePublicId.from_raw(data.public_id)
        exists_profile = self.profile_repository.exists_by_public_id(public_id)
        if exists_profile:
            raise ProfilePublicIdNotAvailable(public_id)

        # Validate & check email
        email = UserEmail.from_raw(data.email)
        exists_user = self.user_repository.exists_by_email(email)
        if exists_user:
            raise EmailAlreadyRegistered(email)

        # Validate superuser permission
        if data.is_superuser:
            if not current_user or not current_user.is_superuser:
                raise ForbiddenAction("create", "superuser")

        # Create the user entity & save to get id from db
        password_hash = self.password_hasher.hash(data.password)
        user = UserFactory.create(
            email = email,
            password_hash = password_hash,
            is_superuser = data.is_superuser
        )
        self.user_repository.save(user)

        # Create the profile entity
        profile = UserProfileFactory.create_for_user(
            user_id = user.id,
            public_id = public_id
        )
        self.profile_repository.save(profile)

        # Link in memory
        user.attach_profile(profile)

        # Persist all changes (user and profile) and refresh the entity state
        self.user_repository.commit()

        # Convert the domain entity to output DTO and return
        return UserOutput.from_entity(user)
