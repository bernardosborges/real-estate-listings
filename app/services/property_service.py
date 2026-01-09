from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from decimal import Decimal

from app.repositories.property_repository import create_property, list_properties, list_properties_by_user, list_properties_in_rectangle, update_property, soft_delete_property, get_property
from app.models.user_model import UserModel
from app.schemas.property_schema import PropertyCreateSchema, PropertyUpdateSchema


# -----------------------------------------------
# CRUD - CREATE
# -----------------------------------------------

def create_property_service(db: Session, property_data: PropertyCreateSchema, user: UserModel):
    property = create_property(db, property_data, user)
    db.commit()
    db.refresh(property)
    return property


# -----------------------------------------------
# CRUD - READ
# -----------------------------------------------

def list_properties_service(
        db: Session,
        price_min: Decimal | None,
        price_max: Decimal | None,
        limit: int,
        offset: int
    ):
    return list_properties(db, price_min, price_max, limit, offset)

def list_properties_by_user_service(
        db: Session,
        user_id: int,
        price_min: Decimal | None,
        price_max: Decimal | None,
        limit: int,
        offset: int
    ):
    return list_properties_by_user(db, user_id, price_min, price_max, limit, offset)

def get_property_service(db: Session, property_id: int):
    return get_property(db, property_id)

def list_properties_for_map_service(
        db: Session,
        min_lat: float,
        max_lat: float,
        min_lng: float,
        max_lng: float,
        price_min: Decimal | None,
        price_max: Decimal | None,
        limit: int = 50,
        offset: int = 0
):
    return list_properties_in_rectangle(db, min_lat, max_lat, min_lng, max_lng, price_min, price_max, limit, offset)


# -----------------------------------------------
# CRUD - UPDATE
# -----------------------------------------------

def update_property_service(db: Session, property_id: int, property_data: PropertyUpdateSchema, user: UserModel):
    property = get_property(db, property_id)
    if not property:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Property not found")
    
    if property.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not own this property")

    updated = update_property(db, property_id, property_data)
    db.commit()
    db.refresh(updated)
    return updated


# -----------------------------------------------
# CRUD - DELETE
# -----------------------------------------------

def delete_property_service(db: Session, property_id: int, user: UserModel):
    property = get_property(db, property_id)
    if not property:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Property not found")
    
    if property.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not own this property")

    deleted = soft_delete_property(db, property_id)
    db.commit()
    return deleted