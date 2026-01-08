from pydantic import BaseModel, EmailStr, field_validator
import re

class UserBaseSchema(BaseModel):
    email: EmailStr

    model_config = {
        "title": "UserBaseSchema",
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "email": "user@userdomain.com"
            }
        }
    }

    @field_validator("email")
    def email_must_be_valid(cls, v):
        if "@" not in v:
            raise ValueError("Invalid email")
        return v

class UserCreateSchema(UserBaseSchema):
    password: str

    @field_validator('password')
    def password_min_lenght(cls, v):
        pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$"
        if not re.match(pattern, v):
            raise ValueError("Password must be at least 8 characteres, a number, a letter and a special character")
        return v
    
class UserLoginSchema(UserBaseSchema):
    password: str

class UserReadSchema(UserBaseSchema):
    id: int
    is_active: bool
    is_verified: bool
    is_superuser: bool