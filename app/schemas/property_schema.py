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
        "from_attributes": True
    }

class PropertyCreateSchema(PropertyBaseSchema):
    pass

class PropertyReadSchema(PropertyBaseSchema):
    id: int