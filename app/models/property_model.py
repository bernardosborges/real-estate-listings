from pydantic import BaseModel

class PropertyCreate(BaseModel):
    description: str
    price: float
    private_area: float
    address: str
    latitude: float
    longitude: float
