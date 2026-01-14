from sqlalchemy.orm import Session
from datetime import datetime, timezone
from decimal import Decimal

from app.models.property_model import PropertyModel
from app.models.user_model import UserModel
from app.models.address_model import AddressModel
from app.schemas.property_schema import PropertyCreateSchema, PropertyUpdateSchema


class PropertyRepository:

    # -----------------------------------------------
    # CRUD - CREATE
    # -----------------------------------------------

    @staticmethod
    def create_property(db: Session, description: str, price: Decimal, private_area: Decimal, user_id: int, address_id: int):
        #data = schema.model_dump() # exclude={"tags_ids"}
        #db_property = PropertyModel(**data, user_id=user_id)
        db_property = PropertyModel(
            description=description,
            price=price,
            private_area=private_area,
            user_id=user_id,
            address_id=address_id
        )
        db.add(db_property)
        db.flush()
        return db_property


    # -----------------------------------------------
    # CRUD - READ
    # -----------------------------------------------

    @staticmethod
    def list_properties(
            db: Session,
            price_min: Decimal,
            price_max: Decimal,
            limit: int = 20,
            offset: int = 0
    ):
        query = db.query(PropertyModel).filter(PropertyModel.is_active == True)
        if price_min is not None:
            query = query.filter(PropertyModel.price >= price_min)
        
        if price_max is not None:
            query = query.filter(PropertyModel.price <= price_max)

        return query.offset(offset).limit(limit).all()

    @staticmethod
    def list_properties_by_user(
            db: Session,
            user_id: int,
            price_min: Decimal,
            price_max: Decimal,
            limit: int = 20,
            offset: int = 0
    ):
        query = db.query(PropertyModel).filter(PropertyModel.user_id == user_id, PropertyModel.is_active == True)
        
        if price_min is not None:
            query = query.filter(PropertyModel.price >= price_min)
        
        if price_max is not None:
            query = query.filter(PropertyModel.price <= price_max)

        return query.offset(offset).limit(limit).all()

    @staticmethod
    def get_property(db: Session, property_id: int) -> PropertyModel | None:
        return db.query(PropertyModel).filter(PropertyModel.id == property_id, PropertyModel.is_active == True).first()

    @staticmethod
    def list_properties_in_rectangle(
            db: Session,
            min_lat: float,
            max_lat: float,
            min_lng: float,
            max_lng: float,
            price_min: float | None = None,
            price_max: float | None = None,
            limit: int = 50,
            offset: int = 0
    ):
        query = db.query(PropertyModel).join(
            AddressModel, 
            PropertyModel.address_id == AddressModel.id).filter(
            AddressModel.latitude.between(min_lat, max_lat),
            AddressModel.longitude.between(min_lng, max_lng),
            PropertyModel.is_active == True
        ).all()

        if price_min is not None:
            query = query.filter(PropertyModel.price >= price_min)
        
        if price_max is not None:
            query = query.filter(PropertyModel.price <= price_max)

        return query.offset(offset).limit(limit).all()


    # -----------------------------------------------
    # CRUD - UPDATE
    # -----------------------------------------------

    @staticmethod
    def update_property(db: Session, property_id: int, property_data: PropertyUpdateSchema):
        db_property = PropertyRepository.get_property(db, property_id)
        if not db_property:
            return None
        
        update_data = property_data.model_dump(exclude_unset=True) # Exclude empty fields

        update_data.pop("address", None)

        for key, value in update_data.items():
            setattr(db_property, key, value)
        
        return db_property


    # -----------------------------------------------
    # CRUD - DELETE
    # -----------------------------------------------

    @staticmethod
    def delete_property(db: Session, property_id: int):
        db_property = PropertyRepository.get_property(db, property_id)
        if not db_property:
            return None
        
        db.delete(db_property)
        return db_property

    @staticmethod
    def soft_delete_property(db: Session, property_id: int):
        db_property = PropertyRepository.get_property(db, property_id)
        if not db_property:
            return None
        
        db_property.deleted_at = datetime.now(timezone.utc)
        db_property.is_active = False

        return db_property