from pydantic import BaseModel
from decimal import Decimal

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