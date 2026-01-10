from sqlalchemy.orm import Session

from app.repositories.address_repository import get_address_by_unique_fields, create_address
from app.models.address_model import AddressModel
from app.schemas.address_schema import AddressCreateSchema


def get_or_create_address(db: Session, address_data: AddressCreateSchema) -> AddressModel | None:
    """
    Retrieves an existing address or create a new one. 
    """
    existing_address = get_address_by_unique_fields(
        db,
        zip_code=address_data.zip_code,
        street=address_data.street,
        number=address_data.number,
        complement=address_data.complement
    )

    if existing_address:
        return existing_address
    
    new_address = create_address(db, address_data)
    return new_address

    