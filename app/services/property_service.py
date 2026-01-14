import httpx
import asyncio
import logging

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from decimal import Decimal

from app.repositories.property_repository import PropertyRepository
from app.models.user_model import UserModel
from app.schemas.property_schema import PropertyCreateSchema, PropertyUpdateSchema
from app.services.address_service import get_or_create_address
from app.services.cep_service import resolve_address_input_async
from app.services.geocoding_service import geocode_address
from app.schemas.address_schema import AddressCreateSchema
from app.core.exceptions.domain_exception import PropertyForbidden, PropertyNotFound

logger = logging.getLogger(__name__)

# -----------------------------------------------
# CRUD - CREATE
# -----------------------------------------------

def create_property_service(db: Session, property_data: PropertyCreateSchema, user: UserModel):
    
    address_data = property_data.address

    lat = None
    lng = None

    try:
        lat, lng = asyncio.run(geocode_address(address_data))
    except Exception as e:
        logger.warning("Geocoding failed during property creation", extra={"zip_code": address_data.zip_code}, exc_info=e)
        #raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="Unable to determine property location")

    address_payload = address_data.model_dump()
    address_payload.pop("latitude", None)
    address_payload.pop("longitude", None)

    address_schema = AddressCreateSchema(**address_payload, latitude=lat, longitude=lng)

    address = get_or_create_address(db, address_schema)
    
    property = PropertyRepository.create_property(
        db,
        description=property_data.description,
        price=property_data.price,
        private_area=property_data.private_area,
        user_id=user.id,
        address_id=address.id)
    
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
    return PropertyRepository.list_properties(db, price_min, price_max, limit, offset)

def list_properties_by_user_service(
        db: Session,
        user_id: int,
        price_min: Decimal | None,
        price_max: Decimal | None,
        limit: int,
        offset: int
    ):
    return PropertyRepository.list_properties_by_user(db, user_id, price_min, price_max, limit, offset)

def get_property_service(db: Session, property_id: int):
    property = PropertyRepository.get_property(db, property_id)
    if not property:
         raise PropertyNotFound()
    return property

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
    return PropertyRepository.list_properties_in_rectangle(db, min_lat, max_lat, min_lng, max_lng, price_min, price_max, limit, offset)


# -----------------------------------------------
# CRUD - UPDATE
# -----------------------------------------------

def update_property_service(db: Session, property_id: int, property_data: PropertyUpdateSchema, user: UserModel):
    db_property = PropertyRepository.update_property(db, property_id, property_data)
    
    if not db_property:
        raise PropertyNotFound()
    
    if db_property.user_id != user.id:
        raise PropertyForbidden()

    address_data = property_data.address
    if address_data:
        address = get_or_create_address(db, address_data)
        db_property.address_id = address.id

    db.commit()
    db.refresh(db_property)
    return db_property


# -----------------------------------------------
# CRUD - DELETE
# -----------------------------------------------

def delete_property_service(db: Session, property_id: int, user: UserModel):
    property = PropertyRepository.get_property(db, property_id)
    if not property:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Property not found")
    
    if property.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not own this property")

    deleted = PropertyRepository.soft_delete_property(db, property_id)
    db.commit()
    return deleted