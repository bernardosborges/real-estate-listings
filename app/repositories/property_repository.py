from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.models.property_model import PropertyModel
from app.models.user_model import UserModel
from app.schemas.property_schema import PropertyCreateSchema, PropertyUpdateSchema


def create_property(db: Session, schema: PropertyCreateSchema, user: UserModel):
    data = schema.model_dump() # exclude={"tags_ids"}
    db_property = PropertyModel(**data, user_id=user.id)
    db.add(db_property)
    return db_property

def list_properties(db: Session):
    return db.query(PropertyModel).filter(PropertyModel.is_active == True).all()

def get_property(db: Session, property_id: int):
    return db.query(PropertyModel).filter(PropertyModel.id == property_id, PropertyModel.is_active == True).first()

def update_property(db: Session, property_id: int, schema: PropertyUpdateSchema):
    db_property = get_property(db, property_id)
    if not db_property:
        return None
    
    update_data = schema.model_dump(exclude_unset=True) # Exclude empty fields
    for key, value in update_data.items():
        setattr(db_property, key, value)
    return db_property

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