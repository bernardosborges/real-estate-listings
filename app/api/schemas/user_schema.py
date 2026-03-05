from pydantic import BaseModel, EmailStr

from app.api.schemas.user_profile_schema import UserProfileResponseSchema
from app.application.dto.user.login_user_output import LoginUserOutput


class CreateUserRequestSchema(BaseModel):
    email: EmailStr
    password: str
    is_superuser: bool | None = False
    public_id: str

    model_config = {
        "title": "CreateUserRequestSchema",
        "from_attributes": True,
    }


class UserResponseSchema(BaseModel):
    email: EmailStr
    is_superuser: bool
    profile: UserProfileResponseSchema

    model_config = {
        "title": "UserResponseSchema",
        "from_attributes": True,
    }


class LoginRequestSchema(BaseModel):
    email: str
    password: str

    model_config = {
        "title": "LoginRequestSchema",
        "from_attributes": True,
    }


class LoginResponseSchema(BaseModel):
    access_token: str
    token_type: str
    user: UserResponseSchema

    model_config = {
        "title": "LoginResponseSchema",
        "from_attributes": True,
    }

    @classmethod
    def from_dto(cls, dto: LoginUserOutput):
        return cls(access_token=dto.access_token, token_type="bearer", user=dto.user)


# class UserBaseSchema(BaseModel):
#     email: EmailStr

#     model_config = {
#         "title": "UserBaseSchema",
#         "from_attributes": True,
#         "json_schema_extra": {
#             "example": {
#                 "email": "user@userdomain.com",
#                 "password": "Abc12345"
#             }
#         }
#     }

#     @field_validator("email")
#     def email_must_be_valid(cls, v):
#         if "@" not in v:
#             raise ValueError("Invalid email")
#         return v

# class UserCreateSchema(UserBaseSchema):
#     password: str

#     @field_validator('password')
#     def password_min_lenght(cls, v):
#         pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$"
#         if not re.match(pattern, v):
#             raise ValueError("Password must be at least 8 characteres, a number, a letter and a special character")
#         return v

# class UserLoginSchema(UserBaseSchema):
#     password: str

# class UserReadSchema(UserBaseSchema):
#     id: int
#     is_active: bool
#     is_verified: bool
#     is_superuser: bool
