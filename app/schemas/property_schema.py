from pydantic import BaseModel
from decimal import Decimal

class PropertyCreateSchema(BaseModel):
    description: str
    price: Decimal
    private_area: Decimal
    address: str
    latitude: Decimal
    longitude: Decimal


    model_config = {
        "from_attributes": True
    }

class PropertyReadSchema(PropertyCreateSchema):
    id: int

    model_config = {
        "from_attributes": True
    }