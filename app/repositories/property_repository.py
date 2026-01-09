from sqlalchemy.orm import Session
from datetime import datetime, timezone
from decimal import Decimal

from app.models.property_model import PropertyModel
from app.models.user_model import UserModel
from app.schemas.property_schema import PropertyCreateSchema, PropertyUpdateSchema


# -----------------------------------------------
# CRUD - CREATE
# -----------------------------------------------

def create_property(db: Session, schema: PropertyCreateSchema, user: UserModel):
    data = schema.model_dump() # exclude={"tags_ids"}
    db_property = PropertyModel(**data, user_id=user.id)
    db.add(db_property)
    return db_property


# -----------------------------------------------
# CRUD - READ
# -----------------------------------------------

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

def get_property(db: Session, property_id: int):
    return db.query(PropertyModel).filter(PropertyModel.id == property_id, PropertyModel.is_active == True).first()

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
    query = db.query(PropertyModel).filter(
        PropertyModel.is_active == True,
        PropertyModel.latitude.between(min_lat, max_lat),
        PropertyModel.longitude.between(min_lng, max_lng)
    )

    if price_min is not None:
        query = query.filter(PropertyModel.price >= price_min)
    
    if price_max is not None:
        query = query.filter(PropertyModel.price <= price_max)

    return query.offset(offset).limit(limit).all()


# -----------------------------------------------
# CRUD - UPDATE
# -----------------------------------------------

def update_property(db: Session, property_id: int, schema: PropertyUpdateSchema):
    db_property = get_property(db, property_id)
    if not db_property:
        return None
    
    update_data = schema.model_dump(exclude_unset=True) # Exclude empty fields
    for key, value in update_data.items():
        setattr(db_property, key, value)
    return db_property


# -----------------------------------------------
# CRUD - DELETE
# -----------------------------------------------

def delete_property(db: Session, property_id: int):
    db_property = get_property(db, property_id)
    if not db_property:
        return None
    
    db.delete(db_property)
    return db_property

def soft_delete_property(db: Session, property_id: int):
    db_property = get_property(db, property_id)
    if not db_property:
        return None
    
    db_property.deleted_at = datetime.now(timezone.utc)
    db_property.is_active = False

    return db_property