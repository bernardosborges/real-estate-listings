from sqlalchemy.orm import Session
from app.repositories.property_repository import create_property, list_properties
from app.schemas.property_schema import PropertyCreateSchema

def create_property_service(db: Session, property_data: PropertyCreateSchema):
    return create_property(db, property_data)

def list_properties_service(db: Session):
    return list_properties(db)