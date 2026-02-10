import httpx
import asyncio
import logging

from typing import List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from decimal import Decimal

from app.infrastructure.storage.s3_service import S3Service
from app.repositories.property_repository import PropertyRepository
from app.models.user_model import UserModel
from app.models.property_model import PropertyModel
from app.schemas.property_schema import PropertyCreateSchema, PropertyUpdateSchema
from app.application.services.auth_service import AuthService
from app.services.address_service import AddressService
from app.services.cep_service import resolve_address_input_async
from app.infrastructure.services.google_geocoding_service import geocode_address
from app.services.user_profile_service import UserProfileService
from app.services.photo_service import PhotoService
from app.schemas.address_schema import AddressCreateSchema
from app.core.exceptions.domain_exception import PropertyForbidden, PropertyNotFound, ForbiddenAction

logger = logging.getLogger(__name__)

class PropertyService:

# -----------------------------------------------
# CRUD - CREATE
# -----------------------------------------------

    @staticmethod
    def create(db: Session, property_data: PropertyCreateSchema, current_user: UserModel) -> PropertyModel:
        
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

        address = AddressService.get_or_create(db, address_schema)
        
        property = PropertyRepository.create(
            db,
            description=property_data.description,
            price=property_data.price,
            private_area=property_data.private_area,
            user_id=current_user.id,
            address_id=address.id)
        
        db.commit()
        db.refresh(property)
        return property


# -----------------------------------------------
# CRUD - READ
# -----------------------------------------------

    @staticmethod
    def get_with_details_by_public_id(db: Session, storage: S3Service, public_id: str) -> PropertyModel:
        db_property = PropertyRepository.get_with_details_by_public_id(db, public_id, is_editing=False)
        if not db_property:
            raise PropertyNotFound()
        
        enriched_photos = PhotoService.enrich_with_thumbnails(db, storage, db_property.photos)
        db_property.enriched_photos = enriched_photos

        return db_property


    @staticmethod
    def get_by_id_or_404(db: Session, id: int, is_active: bool | None = True, include_deleted: bool = False) -> PropertyModel:
        db_property = PropertyRepository.get_by_id(db, id, is_active, include_deleted)
        if not db_property:
            raise PropertyNotFound()
        return db_property
    
    @staticmethod
    def get_by_public_id_or_404(db: Session, public_id: str, is_active: bool | None = True, include_deleted: bool = False) -> PropertyModel:
        db_property = PropertyRepository.get_by_public_id(db, public_id, is_active, include_deleted)
        if not db_property:
            raise PropertyNotFound()
        return db_property

    @staticmethod
    def list_all(
            db: Session,
            price_min: Decimal | None,
            price_max: Decimal | None,
            limit: int,
            offset: int
        ) -> List[PropertyModel]:
        return PropertyRepository.list_all(db, price_min, price_max, limit, offset)

    @staticmethod
    def list_by_user_profile_public_id(
            db: Session,
            user_profile_public_id: str,
            price_min: Decimal | None,
            price_max: Decimal | None,
            limit: int,
            offset: int
        ) -> List[PropertyModel]:
        db_user_profile = UserProfileService.get_by_public_id_or_404(db, user_profile_public_id, include_deleted=False)
        return PropertyRepository.list_by_user_id(db, db_user_profile.public_id, price_min, price_max, limit, offset)

    @staticmethod
    def list_for_map(
            db: Session,
            min_lat: float,
            max_lat: float,
            min_lng: float,
            max_lng: float,
            price_min: Decimal | None,
            price_max: Decimal | None,
            limit: int = 50,
            offset: int = 0
    ) -> List[PropertyModel]:
        return PropertyRepository.list_in_rectangle(db, min_lat, max_lat, min_lng, max_lng, price_min, price_max, limit, offset)


# -----------------------------------------------
# CRUD - UPDATE
# -----------------------------------------------

    @staticmethod
    def update(db: Session, public_id: str, data: dict, current_user: UserModel) -> PropertyModel:
        db_property = PropertyService.get_by_public_id_or_404(db, public_id, is_active=None, include_deleted=False)
        
        AuthService.ensure_owner_or_admin(db_property.user_id, current_user, "update", "property")

        address_data = data.pop("address", None)
        if address_data is not None:
            address = AddressService.get_or_create(db, address_data)
            db_property.address_id = address.id

        update_data = data.model_dump(exclude_unset=True)
        if update_data:
            PropertyRepository.update(db, db_property.id, **update_data)

        db.commit()
        db.refresh(db_property)
        return db_property

    @staticmethod
    def restore(db: Session, public_id: str, current_user: UserModel | None = None) -> PropertyModel:
        db_property = PropertyService.get_by_public_id_or_404(db, public_id, is_active=None, include_deleted=True)

        if current_user is not None:
             AuthService.ensure_owner_or_admin(db_property.user_id, current_user, "restore", "property")
        
        if db_property.deleted_at is None:
            return db_property
        
        PropertyRepository.restore(db, db_property.id)
        db.commit()
        db.refresh(db_property)
        return db_property

# -----------------------------------------------
# CRUD - DELETE
# -----------------------------------------------

    @staticmethod
    def delete(db: Session, public_id: str, current_user: UserModel | None = None):
        db_property = PropertyService.get_by_public_id_or_404(db, public_id, is_active=None, include_deleted=False)
        
        if current_user is not None:
            AuthService.ensure_owner_or_admin(db_property.user_id, current_user, "delete", "property")

        deleted = PropertyRepository.soft_delete(db, db_property.id)
        db.commit()
        return deleted