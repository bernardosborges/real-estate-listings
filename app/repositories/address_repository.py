from sqlalchemy.orm import Session

from app.models.address_model import AddressModel
from app.schemas.address_schema import AddressCreateSchema

# -----------------------------------------------
# CRUD - CREATE
# -----------------------------------------------

def create_address(db: Session, schema: AddressCreateSchema) -> AddressModel:
    data = schema.model_dump()
    address = AddressModel(**data)
    db.add(address)
    db.flush()
    return address


# -----------------------------------------------
# CRUD - READ
# -----------------------------------------------

def get_address_by_unique_fields(db: Session, zip_code: str, street: str, number: str, complement: str | None) -> AddressModel | None:
    """
    Search for an address based on unique fields.
    Return None if do not find.
    """
    return db.query(AddressModel).filter(
        AddressModel.zip_code == zip_code,
        AddressModel.street == street,
        AddressModel.number == number,
        AddressModel.complement == complement
    ).first()

def get_address_by_id(db: Session, address_id: int) -> AddressModel | None:
    """
    Search for address by id.
    """
    return db.query(AddressModel).filter(AddressModel.id == address_id).first()