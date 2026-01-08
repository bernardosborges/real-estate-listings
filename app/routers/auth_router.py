from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.user_schema import UserCreateSchema, UserReadSchema, UserLoginSchema
from app.core.database import get_db
from app.core.config import settings
from app.services.user_service import register_user_service
from app.services.auth_service import authenticate_user_service, generate_token_for_user_service

router = APIRouter(prefix=f"{settings.API_PREFIX}/auth", tags=["Auth"])

# ------------ REGISTER USER ENDPOINT ------------
@router.post(
        "/register",
        response_model=UserReadSchema,
        summary="Register a new user",
        description="Register a new user to the database. Requires a valid email and a 8-digit password.",
        status_code=status.HTTP_201_CREATED
)
def register_user_endpoint(
    user_data: UserCreateSchema,
    db: Session = Depends(get_db)
):
    try:
        return register_user_service(db, user_data.email, user_data.password)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# ------------ LOGIN USER ENDPOINT ------------
@router.post(
        "/login",
        summary="Login a user",
        description="Login a user. Requires a valid email and a password.",
        status_code=status.HTTP_200_OK
)
def login_user_endpoint(
    user_data: UserLoginSchema,
    db: Session = Depends(get_db)
):
    user = authenticate_user_service(db, user_data.email, user_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    return generate_token_for_user_service(user)