from fastapi import APIRouter, Query
from app.models.property_model import PropertyCreate
from app.services.property_service import (
    create_property_service,
    list_properties_service
)

router = APIRouter(prefix="/properties", tags=["Properties"])

@router.post("/")
def create_property(property: PropertyCreate):
    create_property_service(property)
    return {"message": "Property created"}

@router.get("/")
def list_properties(
    min_price: float | None = Query(None),
    max_price: float | None = Query(None)
):
    return list_properties_service({
        "min_price": min_price,
        "max_price": max_price
    })