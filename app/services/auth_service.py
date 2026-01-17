from sqlalchemy.orm import Session

from app.core.security import verify_password, create_access_token
from app.repositories.user_repository import UserRepository
from app.models.user_model import UserModel
from app.core.exceptions.domain_exception import InvalidCredentials

class AuthService:

    @staticmethod
    def authenticate_user_service(db: Session, email: str, password: str):
        user = UserRepository.get_by_email(db, email)
        if not user or not verify_password(password, user.password_hash):
            raise InvalidCredentials()
        return user

    @staticmethod
    def generate_token_for_user_service(user: UserModel):
        access_token = create_access_token(data={"sub":str(user.id)})
        return {"access_token": access_token, "token_type": "bearer"}