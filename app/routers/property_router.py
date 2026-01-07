from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.property_schema import PropertyCreateSchema, PropertyReadSchema
from app.services.property_service import create_property_service, list_properties_service, update_property_service, delete_property_service, get_property_service



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

@router.get(
         "/{property_id}", 
        response_model=PropertyReadSchema,
        summary="Get a property",
        description="Retrieves a property from the database."
)
def get_property_endpoint(property_id: int, db: Session = Depends(get_db)):
    property = get_property_service(db, property_id)
    if not property:
        raise HTTPException(status_code=404, detail="Property not found")
    return property

@router.put(
        "/{property_id}", 
        response_model=PropertyReadSchema,
        summary="Update a property",
        description="Updates a property to the database."
)
def update_property_endpoint(property_id: int, property: PropertyCreateSchema, db: Session = Depends(get_db)):
    updated = update_property_service(db, property_id, property)
    if not updated:
        raise HTTPException(status_code=404, detail="Property not found")
    return updated

@router.delete(
        "/{property_id}", 
        response_model=PropertyReadSchema,
        summary="Delete a property",
        description="Delete a property from the database."
)
def delete_property_endpoint(property_id: int, db: Session = Depends(get_db)):
    deleted = delete_property_service(db, property_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Property not found")
    return deleted