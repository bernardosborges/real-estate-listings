from pydantic import BaseModel, field_validator
from decimal import Decimal
from typing import Optional

from app.schemas.address_schema import AddressCreateSchema, AddressReadSchema

# -----------------------------------------------
# BASE
# -----------------------------------------------

class PropertyBaseSchema(BaseModel):
    description: str
    price: Decimal
    private_area: Decimal

    model_config = {
        "title": "PropertyBaseSchema",
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "description": "Apartamento padrão",
                "price": 250000.00,
                "private_area": 80.00,
                "address": {
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
    }

    @field_validator('price')
    def price_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("Price must be greater than 0")
        return v

    @field_validator('private_area')
    def private_area_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("Private area must be greater than 0")
        return v


# -----------------------------------------------
# CREATE
# -----------------------------------------------

class PropertyCreateSchema(PropertyBaseSchema):
    """
    Schema used to create a new property.
    Inherits all fields from PropertyBaseSchema
    """

    address: AddressCreateSchema

    model_config = {
        **PropertyBaseSchema.model_config,
        "title": "PropertyCreateSchema"
    }

# -----------------------------------------------
# READ
# -----------------------------------------------

class PropertyReadSchema(PropertyBaseSchema):
    """
    Schema used to read a property (response schema).
    Adds the 'id' field returned by the database.
    """
    id: int
    is_active: bool
    address: AddressReadSchema

    model_config = {
        **PropertyBaseSchema.model_config,
        "title": "PropertyReadSchema",
        "json_schema_extra": {
            "example": {
                "id": 1,
                "is_active": True,
                **PropertyBaseSchema.model_config["json_schema_extra"]["example"]
            }
        }
    }

# -----------------------------------------------
# UPDATE
# -----------------------------------------------

class PropertyUpdateSchema(BaseModel):
    description: str | None = None
    price: Decimal | None = None
    private_area: Decimal | None = None
    is_active: bool | None = None

    address: AddressCreateSchema | None = None

    # -------- VALIDATORS --------
    @field_validator('price')
    def price_must_be_positive(cls, v):
        if v is not None and v <= 0:
            raise ValueError("Price must be greater than 0")
        return v

    @field_validator('private_area')
    def private_area_must_be_positive(cls, v):
        if v is not None and v <= 0:
            raise ValueError("Private area must be greater than 0")
        return v