from sqlalchemy.orm import Session
from app.models.property_model import PropertyModel
from app.schemas.property_schema import PropertyCreateSchema


def create_property(db: Session, schema: PropertyCreateSchema):
    data = schema.model_dump() # exclude={"tags_ids"}
    db_property = PropertyModel(**data)
    
    print(">>> ENTROU NO REPOSITORY")
    db.add(db_property)
    print(">>> ADDED PROPERTY")
    return db_property

def list_properties(db: Session):
    return db.query(PropertyModel).all()

