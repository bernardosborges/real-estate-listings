from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.api.deps.general_deps import get_db_session
from app.api.deps.oauth2 import get_current_user, superuser_required

from app.api.schemas.user_schema import CreateUserRequestSchema, UserResponseSchema, LoginRequestSchema, LoginResponseSchema
from app.application.usecases.user.register_user import RegisterUserUseCase
from app.application.usecases.user.login_user import LoginUserUseCase
from app.application.services.token_service import TokenService
from app.application.services.password_hasher_service import PasswordHasher
from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository
from app.domain.repositories.user_profile_repository import UserProfileRepository
from app.infrastructure.db.repositories.user_repository_sqlalchemy import UserRepositorySQLAlchemy
from app.infrastructure.db.repositories.user_profile_repository_sqlalchemy import UserProfileRepositorySQLAlchemy
from app.infrastructure.services.jwt_token_service import JWTTokenService
from app.infrastructure.security.bcrypt_password_hasher import BcryptPasswordHasher


router = APIRouter(prefix=f"{settings.API_PREFIX}/auth", tags=["Auth"])


@router.post(
        "/register",
        response_model=UserResponseSchema,
        summary="Register a new user",
        description="Register a new user to the database. Requires a valid email and a 8-digit password.",
        status_code=status.HTTP_201_CREATED
)
def register_user_endpoint(
    user_input: CreateUserRequestSchema,
    db: Session = Depends(get_db_session),
    #current_user: User = Depends(get_current_user)
):
    user_repository: UserRepository = UserRepositorySQLAlchemy(db)
    profile_repository: UserProfileRepository = UserProfileRepositorySQLAlchemy(db)
    password_hasher: PasswordHasher = BcryptPasswordHasher()

    register_usecase = RegisterUserUseCase(
        user_repository = user_repository,
        profile_repository = profile_repository,
        password_hasher = password_hasher
    )

    created_user = register_usecase.execute(data=user_input, current_user=None)
    return created_user


@router.post(
        "/login",
        response_model=LoginResponseSchema,
        summary="Login a user",
        description="Login a user. Requires a valid email and a password.",
        status_code=status.HTTP_200_OK
)
def login_user_endpoint(
    user_input: LoginRequestSchema,
    db: Session = Depends(get_db_session)
):
    user_repository: UserRepository = UserRepositorySQLAlchemy(db)
    token_service: TokenService = JWTTokenService()
    password_hasher: PasswordHasher = BcryptPasswordHasher()

    login_usecase = LoginUserUseCase(
        user_repository=user_repository,
        token_service=token_service,
        password_hasher=password_hasher
    )
    result_dto = login_usecase.execute(data=user_input)
    
    return LoginResponseSchema.from_dto(result_dto)



# # -----------------------------------------------
# # ENDPOINT - REGISTER USER
# # -----------------------------------------------

# @router.post(
#         "/register",
#         response_model=UserReadSchema,
#         summary="Register a new user",
#         description="Register a new user to the database. Requires a valid email and a 8-digit password.",
#         status_code=status.HTTP_201_CREATED
# )
# def register_user_endpoint(
#     user_data: UserCreateSchema,
#     db: Session = Depends(get_db_session)
# ):
#     try:
#         return UserService.register_user_service(db, user_data.email, user_data.password)
#     except ValueError as e:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# # -----------------------------------------------
# # ENDPOINT - LOGIN USER
# # -----------------------------------------------

# @router.post(
#         "/login",
#         summary="Login a user",
#         description="Login a user. Requires a valid email and a password.",
#         status_code=status.HTTP_200_OK
# )
# def login_user_endpoint(
#     user_data: UserLoginSchema,
#     db: Session = Depends(get_db_session)
# ):
#     user = AuthService.authenticate_user_service(db, user_data.email, user_data.password)
#     if not user:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

#     return AuthService.generate_token_for_user_service(user)