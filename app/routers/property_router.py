from fastapi import APIRouter, Depends, HTTPException, status, Security, Query
from sqlalchemy.orm import Session
from decimal import Decimal

from app.core.database import get_db
from app.core.config import settings
from app.core.oauth2 import get_current_user
from app.models.user_model import UserModel
from app.schemas.property_schema import PropertyCreateSchema, PropertyReadSchema, PropertyUpdateSchema
from app.services.property_service import create_property_service, list_properties_service, list_properties_by_user_service, update_property_service, delete_property_service, get_property_service



router = APIRouter(prefix=f"{settings.API_PREFIX}/properties", tags=["Properties"])


# -----------------------------------------------
# ENDPOINT - CREATE PROPERTY
# -----------------------------------------------

@router.post(
        "/", 
        response_model=PropertyReadSchema,
        summary="Create a new property",
        description="Adds a new property to the database. Requires description, price, private area, address, latitude and longitude."
)
def create_property_endpoint(
    property: PropertyCreateSchema,
    db: Session = Depends(get_db),
    current_user: UserModel = Security(get_current_user)
):
    return create_property_service(db, property, current_user)


# -----------------------------------------------
# ENDPOINT - LIST PROPERTIES
# -----------------------------------------------

@router.get(
        "/",
        response_model=list[PropertyReadSchema],
        summary="List all properties",
        description="Retrieves a paginated list of all active properties in the database. You can filter or paginate results"
)
def list_properties_endpoint(
    db: Session = Depends(get_db),
    price_min: Decimal | None = Query(None, ge=0, description="Minimum price"),
    price_max: Decimal | None = Query(None, ge=0, description="Maximum price"),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of results"),
    offset: int = Query(0, ge=0, description="Number of results do skip")
):
    return list_properties_service(db, price_min, price_max, limit, offset)


# -----------------------------------------------
# ENDPOINT - LIST PROPERTIES BY USER
# -----------------------------------------------

@router.get(
        "/user/{user_id}",
        response_model=list[PropertyReadSchema],
        summary="List all properties from a user with filters",
        description="Retrieves a paginated list of all active properties created by a specific user in the database. You can filter or paginate results."
)
def list_properties_by_user_endpoint(
    user_id: int,
    db: Session = Depends(get_db),
    price_min: Decimal | None = Query(None, ge=0, description="Minimum price"),
    price_max: Decimal | None = Query(None, ge=0, description="Maximum price"),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of results"),
    offset: int = Query(0, ge=0, description="Number of results do skip")
):
    return list_properties_by_user_service(db, user_id, price_min, price_max, limit, offset)


# -----------------------------------------------
# ENDPOINT - GET A PROPERTY
# -----------------------------------------------

@router.get(
         "/{property_id}", 
        response_model=PropertyReadSchema,
        summary="Get a property",
        description="Retrieves a property from the database."
)
def get_property_endpoint(property_id: int, db: Session = Depends(get_db)):
    property = get_property_service(db, property_id)
    if not property:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Property not found")
    return property



# -----------------------------------------------
# ENDPOINT - UPDATE A PROPERTY
# -----------------------------------------------

@router.patch(
        "/{property_id}", 
        response_model=PropertyUpdateSchema,
        summary="Update a property",
        description="Updates a property to the database."
)
def update_property_endpoint(
    property_id: int,
    property: PropertyUpdateSchema,
    db: Session = Depends(get_db),
    current_user: UserModel = Security(get_current_user)
):
    updated = update_property_service(db, property_id, property, current_user)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Property not found")
    return updated


# -----------------------------------------------
# ENDPOINT - DELETE A PROPERTY
# -----------------------------------------------

@router.delete(
        "/{property_id}", 
        response_model=PropertyReadSchema,
        summary="Delete a property",
        description="Delete a property from the database."
)
def delete_property_endpoint(
    property_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Security(get_current_user)
):
    deleted = delete_property_service(db, property_id, current_user)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Property not found")
    return deleted