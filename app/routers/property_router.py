from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.property_schema import PropertyCreateSchema, PropertyReadSchema
from app.services.property_service import create_property_service, list_properties_service


router = APIRouter(prefix="/properties", tags=["Properties"])

@router.post("/", response_model=PropertyReadSchema)
def create_property_endpoint(property: PropertyCreateSchema, db: Session = Depends(get_db)):
    return create_property_service(db, property)

@router.get("/", response_model=list[PropertyReadSchema])
def list_properties_endpoint(db: Session = Depends(get_db)):
    return list_properties_service(db)