# from app.core.security import verify_password, create_access_token
# from app.domain.repositories.user_repository import UserRepository
from app.domain.entities.user import User
from app.domain.exceptions.auth_exceptions import ForbiddenAction


class AuthService:

    # @staticmethod
    # def authenticate_user_service(user_repository: UserRepository, email: str, password: str):
    #     user = user_repository.get_by_email(email)
    #     if not user or not verify_password(password, user.password_hash):
    #         raise InvalidCredentials()
    #     return user

    # @staticmethod
    # def generate_token_for_user_service(user: User):
    #     access_token = create_access_token(data={"sub":str(user.id)})
    #     return {"access_token": access_token, "token_type": "bearer"}

    # -----------------------------------------------
    # OWNERSHIP OR ADMIN
    # -----------------------------------------------
    @staticmethod
    def ensure_owner_or_admin(owner_user_id: int, current_user: User, action: str, resource: str) -> None:
        if owner_user_id == current_user.id:
            return

        if current_user.is_superuser:
            return

        raise ForbiddenAction(action, resource)
