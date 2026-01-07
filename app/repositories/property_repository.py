from sqlalchemy.orm import Session
from app.models.property_model import PropertyModel
from app.schemas.property_schema import PropertyCreateSchema


def create_property(db: Session, schema: PropertyCreateSchema):
    data = schema.model_dump() # exclude={"tags_ids"}
    db_property = PropertyModel(**data)
    db.add(db_property)
    return db_property

def list_properties(db: Session):
    return db.query(PropertyModel).all()

def get_property(db: Session, property_id: int):
    return db.query(PropertyModel).filter(PropertyModel.id == property_id).first()

def update_property(db: Session, property_id: int, schema: PropertyCreateSchema):
    db_property = db.query(PropertyModel).filter(PropertyModel.id == property_id).first()
    if not db_property:
        return None
    
    for key, value in schema.model_dump().items():
        setattr(db_property, key, value)
    return db_property

def delete_property(db: Session, property_id: int):
    db_property = db.query(PropertyModel).filter(PropertyModel.id == property_id).first()
    if not db_property:
        return None
    
    db.delete(db_property)
    return db_property