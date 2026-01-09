from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.property_repository import create_property, list_properties, update_property, delete_property, get_property
from app.models.user_model import UserModel
from app.schemas.property_schema import PropertyCreateSchema, PropertyUpdateSchema

def create_property_service(db: Session, property_data: PropertyCreateSchema, user: UserModel):
    property = create_property(db, property_data, user)
    db.commit()
    db.refresh(property)
    return property

def list_properties_service(db: Session):
    return list_properties(db)

def get_property_service(db: Session, property_id: int):
    return get_property(db, property_id)

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

def delete_property_service(db: Session, property_id: int, user: UserModel):
    property = get_property(db, property_id)
    if not property:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Property not found")
    
    if property.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not own this property")

    delete_property(db, property_id)
    db.commit()
    return property