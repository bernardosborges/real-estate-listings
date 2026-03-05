import re

from pydantic import BaseModel, field_validator
from decimal import Decimal

# -----------------------------------------------
# LOOKUP
# -----------------------------------------------


class LookupAddressResponseSchema(BaseModel):
    zip_code: str
    country: str
    state: str
    city: str
    neighborhood: str | None = None
    street: str | None = None

    model_config = {
        "title": "LookupAddressResponseSchema",
        "from_attributes": True,
    }


# -----------------------------------------------
# BASE
# -----------------------------------------------


class AddressBaseSchema(BaseModel):
    zip_code: str
    country: str = "BR"
    state: str
    city: str
    neighborhood: str | None
    street: str
    number: str
    complement: str | None = None

    latitude: Decimal | None = None
    longitude: Decimal | None = None
    confidence: float | None = None
    provider: str | None = None

    model_config = {
        "title": "AddressBaseSchema",
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "zip_code": "90000000",
                "country": "BR",
                "state": "RS",
                "city": "Porto Alegre",
                "neighborhood": "Centro",
                "street": "Rua das Flores",
                "number": "80",
                "complement": "Apto 301",
                "latitude": -30.0346,
                "longitude": -51.2177,
                "confidence": 1.0,
                "provider": "google",
            }
        },
    }

    @field_validator("zip_code", mode="before")
    def normalize_and_validate_zip_code(cls, v):
        if not v:
            raise ValueError("Zip code is required.")
        digits = re.sub(r"\D", "", v.strip())
        if len(digits) != 8:
            raise ValueError("Invalid zip code. It must contain exactly 8 digits.")
        return digits

    @field_validator("country", "state", mode="before")
    def normalize_country_and_state(cls, v, field):
        if not v:
            raise ValueError(f"{field.name} is required.")
        value = v.strip().upper()
        if len(value) != 2:
            raise ValueError(f"Invalid {field.name}. It  must contain exactly 2 characters.")
        return value

    @field_validator("city", "neighborhood", "street", mode="before")
    def normalize_validade_text_fields(cls, v):
        if v:
            return " ".join(v.strip().split())
        return v

    @field_validator("latitude")
    def latitude_must_be_valid(cls, v):
        if v is not None and not (-90 <= v <= 90):
            raise ValueError("Latitude must be between -90 and 90")
        return v

    @field_validator("longitude")
    def longitude_must_be_valid(cls, v):
        if v is not None and not (-180 <= v <= 180):
            raise ValueError("Longitude must be between -180 and 180")
        return v


# -----------------------------------------------
# BASE
# -----------------------------------------------


class AddressUpdateSchema(BaseModel):
    number: str | None = None
    complement: str | None = None

    latitude: Decimal | None = None
    longitude: Decimal | None = None
    confidence: float | None = None
    provider: str | None = None

    model_config = {
        "title": "AddressUpdateSchema",
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "number": "80",
                "complement": "Apto 301",
                "latitude": -30.0346,
                "longitude": -51.2177,
                "confidence": 1.0,
                "provider": "google",
            }
        },
    }

    @field_validator("latitude")
    def latitude_must_be_valid(cls, v):
        if v is not None and not (-90 <= v <= 90):
            raise ValueError("Latitude must be between -90 and 90")
        return v

    @field_validator("longitude")
    def longitude_must_be_valid(cls, v):
        if v is not None and not (-180 <= v <= 180):
            raise ValueError("Longitude must be between -180 and 180")
        return v


class AddressUpdateResponseSchema(BaseModel):
    zip_code: str
    country: str = "BR"
    state: str
    city: str
    neighborhood: str | None
    street: str
    number: str
    complement: str | None = None

    latitude: Decimal | None = None
    longitude: Decimal | None = None
    confidence: float | None = None
    provider: str | None = None

    model_config = {
        "title": "AddressUpdateResponseSchema",
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "zip_code": "90000000",
                "country": "BR",
                "state": "RS",
                "city": "Porto Alegre",
                "neighborhood": "Centro",
                "street": "Rua das Flores",
                "number": "80",
                "complement": "Apto 301",
                "latitude": -30.0346,
                "longitude": -51.2177,
                "confidence": 1.0,
                "provider": "google",
            }
        },
    }


# class AddressBaseSchema(BaseModel):
#     zip_code: str
#     country: str = "BR"
#     state: str
#     city: str
#     neighborhood: str
#     street: str
#     number: str
#     complement: str | None = None

#     latitude: Decimal | None = None
#     longitude: Decimal | None = None

#     model_config = {
#         "title": "AddressBaseSchema",
#         "from_attributes": True,
#         "json_schema_extra": {
#             "example": {
#                 "zip_code": "90000000",
#                 "country": "BR",
#                 "state": "RS",
#                 "city": "Porto Alegre",
#                 "neighborhood": "Centro",
#                 "street": "Rua das Flores",
#                 "number": "80",
#                 "complement": "Apto 301",
#                 "latitude": -30.0346,
#                 "longitude": -51.2177
#             }
#         }
#     }

#     @field_validator('latitude')
#     def latitude_must_be_valid(cls, v):
#         if v is not None and not (-90 <= v <= 90):
#             raise ValueError("Latitude must be between -90 and 90")
#         return v

#     @field_validator('longitude')
#     def longitude_must_be_valid(cls, v):
#         if v is not None and not (-180 <= v <= 180):
#             raise ValueError("Longitude must be between -180 and 180")
#         return v


# # -----------------------------------------------
# # CREATE
# # -----------------------------------------------

# class AddressCreateSchema(AddressBaseSchema):
#     zip_code: str
#     country: str = "BR"
#     state: str
#     city: str
#     neighborhood: str
#     street: str
#     number: str
#     complement: str | None = None

#     latitude: Decimal | None = None
#     longitude: Decimal | None = None


#     model_config = {
#         **AddressBaseSchema.model_config,
#         "title": "AddressCreateSchema"
#     }

#     @field_validator("zip_code", mode="before")
#     def normalize_and_validate_zip_code(cls, v):
#         if v is None:
#             raise ValueError("Zip code is required.")
#         digits = re.sub(r"\D", "", v)
#         if len(digits) != 8:
#             raise ValueError("Invalid zip code. It must contains exactly 8 digits")
#         return digits


# # -----------------------------------------------
# # READ
# # -----------------------------------------------

# class AddressReadSchema(AddressBaseSchema):
#     id: int

#     model_config = {
#         **AddressBaseSchema.model_config,
#         "title": "AddressReadSchema",
#         "json_schema_extra": {
#             "example": {
#                 "id": 1,
#                 **AddressBaseSchema.model_config["json_schema_extra"]["example"]
#             }
#         }
#     }

# class AddressLookupSchema(BaseModel):
#     zip_code: str
#     country: str = "BR"
#     state: str | None = None
#     city: str | None = None
#     neighborhood: str | None = None
#     street: str | None = None

# # -----------------------------------------------
# # UPDATE
# # -----------------------------------------------
