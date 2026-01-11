from pydantic import BaseModel, Field, field_validator
from decimal import Decimal
import re

# -----------------------------------------------
# BASE
# -----------------------------------------------

class AddressBaseSchema(BaseModel):
    zip_code: str
    country: str = "BR"
    state: str
    city: str
    neighborhood: str
    street: str
    number: str
    complement: str | None = None

    latitude: Decimal | None = None
    longitude: Decimal | None = None

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
                "longitude": -51.2177
            }
        }
    }
    
    @field_validator('latitude')
    def latitude_must_be_valid(cls, v):
        if v is not None and not (-90 <= v <= 90):
            raise ValueError("Latitude must be between -90 and 90")
        return v

    @field_validator('longitude')
    def longitude_must_be_valid(cls, v):
        if v is not None and not (-180 <= v <= 180):
            raise ValueError("Longitude must be between -180 and 180")
        return v


# -----------------------------------------------
# CREATE
# -----------------------------------------------

class AddressCreateSchema(AddressBaseSchema):
    zip_code: str
    country: str = "BR"
    state: str | None = None
    city: str | None = None
    neighborhood: str | None = None
    street: str | None = None
    number: str | None = None
    complement: str | None = None

    latitude: Decimal | None = None
    longitude: Decimal | None = None



    model_config = {
        **AddressBaseSchema.model_config,
        "title": "AddressCreateSchema"
    }

    @field_validator("zip_code", mode="before")
    def normalize_and_validate_zip_code(cls, v):
        if v is None:
            raise ValueError("Zip code is required.")
        digits = re.sub(r"\D", "", v)
        if len(digits) != 8:
            raise ValueError("Invalid zip code. It must contains exactly 8 digits")
        return digits


# -----------------------------------------------
# READ
# -----------------------------------------------

class AddressReadSchema(AddressBaseSchema):
    id: int

    model_config = {
        **AddressBaseSchema.model_config,
        "title": "AddressReadSchema",
        "json_schema_extra": {
            "example": {
                "id": 1,
                **AddressBaseSchema.model_config["json_schema_extra"]["example"]
            }
        }
    }

# -----------------------------------------------
# UPDATE
# -----------------------------------------------
