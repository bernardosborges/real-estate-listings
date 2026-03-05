from sqlalchemy.orm import Session

from app.repositories.address_repository import AddressRepository
from app.models.address_model import AddressModel
from app.schemas.address_schema import AddressCreateSchema


class AddressService:

    @staticmethod
    def get_or_create(db: Session, address_data: AddressCreateSchema) -> AddressModel | None:
        """
        Retrieves an existing address or create a new one.
        """
        db_existing_address = AddressRepository.get_by_unique_fields(
            db,
            zip_code=address_data.zip_code,
            street=address_data.street,
            number=address_data.number,
            complement=address_data.complement,
        )

        if db_existing_address:
            return db_existing_address

        new_address = AddressRepository.create(db, address_data)
        return new_address
