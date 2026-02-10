from pydantic import BaseModel, field_validator, Field, AnyUrl
from typing import Any
import re

#from app.core.exceptions.domain_exception import InvalidPublicId, InvalidWorkPhone


class UserProfileResponseSchema(BaseModel):
    public_id: str
    name: str | None
    bio: str | None
    work_phone: str | None = None,
    work_city: str | None = None,
    license_number: str | None = None,
    profile_picture_url: str | None = None,
    background_image_url: str | None = None,
    preferences: dict | None = None

    model_config = {
         "title": "UserProfileResponseSchema",
         "from_attributes": True,
    }

# # -----------------------------------------------
# # BASE
# # -----------------------------------------------

# class UserProfileBaseSchema(BaseModel):
#     user_id: int

#     model_config = {
#         "title": "UserProfileBaseSchema",
#         "from_attributes": True,
#         "json_schema_extra": {
#             "example": {
#                 "user_id": "unique_user_id"
#             }
#         }
#     }

# # -----------------------------------------------
# # CREATE
# # -----------------------------------------------

# class UserProfileCreateSchema(BaseModel):
#     public_id: str = Field(..., min_length=4, max_length=30)

#     model_config = {
#         "title": "UserProfileCreateSchema",
#         "from_attributes": True,
#         "json_schema_extra": {
#             "example": {
#                 "public_id": "unique_profile_id"
#             }
#         }
#     }

#     @field_validator("public_id")
#     @classmethod
#     def public_id_must_be_valid(clv, v: str):
#         v = v.lower().strip()
#         pattern = r'^[a-z0-9_.]+$'
#         if not re.fullmatch(pattern,v):
#             raise InvalidPublicId()
#         return v

# # -----------------------------------------------
# # READ
# # -----------------------------------------------

# class UserProfileReadSchema(BaseModel):
#     public_id: str = Field(..., min_length=4, max_length=30)
#     name: str | None = Field(None, max_length=100)
#     bio: str | None  = Field(None, max_length=500)
#     work_phone: str | None  = Field(None, max_length=20)
#     work_city: str | None  = Field(None, max_length=100)
#     license_number: str | None  = Field(None, max_length=50)
#     profile_picture_url: AnyUrl | None  = None
#     background_image_url: AnyUrl | None  = None
#     preferences: dict[str, Any] | None = None

#     model_config = {
#         "title": "UserProfileReadSchema",
#         "from_attributes": True,
#         "json_schema_extra": {
#             "example": {
#                 "public_id": "unique_profile_id",
#                 "name": "Mr. Barth Simpsons",
#                 "work_phone": "+55(11)99999-9999",
#                 "work_city": "São Paulo",
#                 "license_number": "CRECI-SP 452456",
#                 "profile_picture_url": "https://hisprofileurl.com/IsTrasbYa23ASf",
#                 "background_image_url": "https://hisbackgroundimageurl.com/7Yggadr5Adv"
#             }
#         }
#     }


# # -----------------------------------------------
# # UPDATE
# # -----------------------------------------------

# class UserProfileUpdateSchema(BaseModel):
#     #new_public_id: str = Field(..., min_length=4, max_length=30)
#     name: str | None = Field(None, max_length=100)
#     bio: str | None = Field(None, max_length=500)
#     work_phone: str | None = Field(None, max_length=20)
#     work_city: str | None = Field(None, max_length=100)
#     license_number: str | None = Field(None, max_length=50)
#     profile_picture_url: AnyUrl | None = None
#     background_image_url: AnyUrl | None = None
#     preferences: dict[str, Any] | None

#     model_config = {
#         "title": "UserProfileUpdateSchema",
#         "from_attributes": True,
#         "json_schema_extra": {
#             "example": {
#                 "name": "Mr. Barth Simpsons",
#                 "bio": "Hello, there!",
#                 "work_phone": "+55(11)99999-9999",
#                 "work_city": "São Paulo",
#                 "license_number": "CRECI-SP 452456",
#                 "profile_picture_url": "https://hisprofileurl.com/IsTrasbYa23ASf",
#                 "background_image_url": "https://hisbackgroundimageurl.com/7Yggadr5Adv"
#             }
#         }
#     }

#     # @field_validator("new_public_id")
#     # def public_id_must_be_valid(clv, v: str):
#     #     v = v.lower().strip()
#     #     pattern = r'^[a-z0-9_.]+$'
#     #     if not re.fullmatch(pattern,v):
#     #         raise InvalidPublicId()
#     #     return v

#     @field_validator("work_phone")
#     @classmethod
#     def work_phone_must_be_valid(clv, v: str | None):
#         if v is None:
#             return v
#         pattern = r"^\+\d{1,3}\d{8,14}$"
#         if not re.fullmatch(pattern,v):
#             raise InvalidWorkPhone("Work phone must be in the format +[1,3][8,14]")
        
#         return v
    
#     @field_validator("name", "bio", "work_city", "license_number")
#     @classmethod
#     def strip_strings(cls, v):
#         return v.strip() if isinstance(v, str) else v
    


# # -----------------------------------------------
# # DELETE
# # -----------------------------------------------