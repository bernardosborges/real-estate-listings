from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.property_schema import PropertyCreateSchema, PropertyReadSchema
from app.services.property_service import create_property_service, list_properties_service



router = APIRouter(prefix="/properties", tags=["Properties"])

@router.post(
        "/", 
        response_model=PropertyReadSchema,
        summary="Create a new property",
        description="Adds a new property to the database. Requires description, price, private area, address, latitude and longitude."
)
def create_property_endpoint(property: PropertyCreateSchema, db: Session = Depends(get_db)):
    return create_property_service(db, property)

@router.get(
        "/",
        response_model=list[PropertyReadSchema],
        summary="List all properties",
        description="Retrieves a paginated list of all properties in the database. You can filter or paginate results in future versions"
)
def list_properties_endpoint(db: Session = Depends(get_db)):
    return list_properties_service(db)