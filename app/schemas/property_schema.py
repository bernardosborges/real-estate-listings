from pydantic import BaseModel, field_validator
from decimal import Decimal
from typing import Optional

class PropertyBaseSchema(BaseModel):
    description: str
    price: Decimal
    private_area: Decimal
    address: str
    latitude: Decimal | None = None
    longitude: Decimal | None = None


    model_config = {
        "title": "PropertyBaseSchema",
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "description": "Apartamento padrão",
                "price": 250000.00,
                "private_area": 80.00,
                "address": "Rua das Flores, 80",
                "latitude": -30.0346,
                "longitude": -51.2177
            }
        }
    }

    # -------- VALIDATORS --------
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

class PropertyCreateSchema(PropertyBaseSchema):
    """
    Schema used to create a new property.
    Inherits all fields from PropertyBaseSchema
    """
    model_config = {
        **PropertyBaseSchema.model_config,
        "title": "PropertyCreateSchema"
    }

class PropertyReadSchema(PropertyBaseSchema):
    """
    Schema used to read a property (response schema).
    Adds the 'id' field returned by the database.
    """
    id: int

    model_config = {
        **PropertyBaseSchema.model_config,
        "title": "PropertyReadSchema",
        "json_schema_extra": {
            "example": {
                **PropertyBaseSchema.model_config["json_schema_extra"]["example"],
                "id": 1
            }
        }
    }

class PropertyUpdateSchema(BaseModel):
    description: Optional[str] = None
    price: Optional[Decimal] = None
    private_area: Optional[Decimal] = None
    address: Optional[str] = None
    latitude: Optional[Decimal] = None
    longitude: Optional[Decimal] = None

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