from sqlalchemy.orm import Session
from app.repositories.property_repository import create_property, list_properties, update_property, delete_property, get_property
from app.schemas.property_schema import PropertyCreateSchema

def create_property_service(db: Session, property_data: PropertyCreateSchema):
    property = create_property(db, property_data)
    db.commit()
    db.refresh(property)
    return property

def list_properties_service(db: Session):
    return list_properties(db)

def get_property_service(db: Session, property_id: int):
    return get_property(db, property_id)

def update_property_service(db: Session, property_id: int, property_data: PropertyCreateSchema):
    property = update_property(db, property_id, property_data)
    db.commit()
    db.refresh(property)
    return property

def delete_property_service(db: Session, property_id: int):
    property = delete_property(db, property_id)
    if property:
        db.commit()
    return property