from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.user_schema import UserCreateSchema, UserReadSchema, UserLoginSchema
from app.core.database import get_db
from app.services.user_service import register_user_service, login_user_service

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post(
        "/register",
        response_model=UserReadSchema,
        summary="Register a new user",
        description="Register a new user to the database. Requires a valid email and a 8-digit password.",
        status_code=201
)
def register_user_endpoint(user_data: UserCreateSchema, db: Session = Depends(get_db)):
    try:
        return register_user_service(db, user_data.email, user_data.password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post(
        "/login",
        summary="Login a user",
        description="Login a user. Requires a valid email and a password.",
        status_code=200
)
def login_user_endpoint(user_data: UserLoginSchema, db: Session = Depends(get_db)):
    result = login_user_service(db, user_data.email, user_data.password)
    if not result:
        raise HTTPException(status_code=401, detail="User or password are invalid")
    return result