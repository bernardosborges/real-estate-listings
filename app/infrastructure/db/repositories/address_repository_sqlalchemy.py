from typing import List
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from psycopg.errors import UniqueViolation

from app.domain.entities.address import Address
from app.domain.repositories.address_repository import AddressRepository
from app.domain.value_objects.address.zipcode import ZipCode
from app.domain.enums.address_enum import CountryEnum, StateEnum
from app.infrastructure.db.models.address_model import AddressModel
from app.infrastructure.db.models.property_model import PropertyModel
from app.infrastructure.db.mappers.address_mapper import AddressMapper
from app.domain.exceptions.address_exceptions import AddressNotFound


class AddressRepositorySQLAlchemy(AddressRepository):

    # -----------------------------------------------
    # INIT
    # -----------------------------------------------

    def __init__(self, db: Session):
        self.db = db

    # -----------------------------------------------
    # METHODS
    # -----------------------------------------------

    def commit(self):
        self.db.commit()

    def refresh(self, address: Address) -> Address:
        model = self.db.get(AddressModel, address.id)
        if not model or model.deleted_at:
            return None

        self.db.refresh(model)
        refreshed_address = AddressMapper.to_entity(model)

        return AddressMapper.update_entity(address, refreshed_address)

    def save(self, address: Address) -> Address:
        if address.id is None:
            model = AddressMapper.to_model(address)
            self.db.add(model)
        else:
            model = self.db.get(AddressModel, address.id)
            if not model or model.deleted_at is not None:
                raise AddressNotFound(
                    f"Address not found or deleted: public id {address.id}."
                )
            AddressMapper.update_model(model, address)

        try:
            self.db.flush()
            return AddressMapper.update_entity(address, AddressMapper.to_entity(model))
        except IntegrityError as exc:
            self.db.rollback()

            raise

    def get_by_id(self, id: int) -> Address | None:
        stmt = select(AddressModel).where(
            AddressModel.id == id,
            AddressModel.deleted_at.is_(None),
        )

        result = self.db.execute(stmt).scalar_one_or_none()

        return AddressMapper.to_entity(result) if result else None

    def get_by_property_id(self, id: int) -> Address | None:
        stmt = (
            select(AddressModel)
            .join(PropertyModel, PropertyModel.address_id == AddressModel.id)
            .where(
                PropertyModel.id == id,
                PropertyModel.deleted_at.is_(None),
                AddressModel.deleted_at.is_(None),
            )
        )

        result = self.db.execute(stmt).scalar_one_or_none()

        return AddressMapper.to_entity(result) if result else None

    def get_by_full_address(
        self,
        zip_code: ZipCode,
        country: CountryEnum,
        state: StateEnum,
        city: str,
        neighborhood: str,
        street: str,
        number: str,
        complement: str | None = None,
    ) -> Address | None:

        conditions = [
            AddressModel.zip_code == zip_code.value,
            AddressModel.country == country.value,
            AddressModel.state == state.value,
            func.lower(AddressModel.city) == city.lower(),
            func.lower(AddressModel.neighborhood) == neighborhood.lower(),
            func.lower(AddressModel.street) == street.lower(),
            func.lower(AddressModel.number) == number.lower(),
            AddressModel.deleted_at.is_(None),
        ]

        if complement is None:
            conditions.append(AddressModel.complement.is_(None))
        else:
            conditions.append(func.lower(AddressModel.complement) == complement.lower())

        stmt = select(AddressModel).where(*conditions)

        result = self.db.execute(stmt).scalar_one_or_none()
        if result is None:
            return None

        return AddressMapper.to_entity(result)

        # AddressModel.zip_code == zip_code.value,
        #         AddressModel.country == country.value,
        #         AddressModel.state == state.value,
        #         func.lower(AddressModel.city) == city.lower(),
        #         func.lower(AddressModel.neighborhood) == neighborhood.lower(),
        #         func.lower(AddressModel.street) == street.lower(),
        #         func.lower(AddressModel.number) == number.lower(),
        #         func.coalesce(func.lower(AddressModel.complement), "") == (complement.lower() if complement else "")


# class AddressRepository:

# # -----------------------------------------------
# # CRUD - CREATE
# # -----------------------------------------------

#     def create(db: Session, schema: AddressCreateSchema) -> AddressModel:
#         data = schema.model_dump()
#         address = AddressModel(**data)
#         db.add(address)
#         db.flush()
#         return address


# # -----------------------------------------------
# # CRUD - READ
# # -----------------------------------------------

#     def get_by_unique_fields(db: Session, zip_code: str, street: str, number: str, complement: str | None, include_deleted: bool = False) -> AddressModel | None:
#         """
#         Search for an address based on unique fields.
#         Return None if do not find.
#         """
#         query = db.query(AddressModel).filter(
#             AddressModel.zip_code == zip_code,
#             AddressModel.street == street,
#             AddressModel.number == number,
#             AddressModel.complement == complement
#         )

#         if not include_deleted:
#             query = query.filter(AddressModel.deleted_at.is_(None))

#         return query.first()

#     def get_by_id(db: Session, id: int, include_deleted: bool = False) -> AddressModel | None:
#         """
#         Search for address by id.
#         """
#         query = db.query(AddressModel).filter(AddressModel.id == id)
#         if not include_deleted:
#                 query = query.filter(AddressModel.deleted_at.is_(None))

#         return query.first()
