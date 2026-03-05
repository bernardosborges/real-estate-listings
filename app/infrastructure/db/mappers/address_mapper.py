from app.domain.entities.address import Address
from app.infrastructure.db.models.address_model import AddressModel


class AddressMapper:

    @staticmethod
    def to_entity(model: AddressModel) -> Address:
        return Address(
            id=model.id,
            zip_code=model.zip_code,
            country=model.country,
            state=model.state,
            city=model.city,
            neighborhood=model.neighborhood,
            street=model.street,
            number=model.number,
            complement=model.complement,
            latitude=model.latitude,
            longitude=model.longitude,
            deleted_at=model.deleted_at,
        )

    @staticmethod
    def to_model(entity: Address) -> AddressModel:
        return AddressModel(
            id=entity.id,
            zip_code=entity.zip_code.value,
            country=entity.country.value,
            state=entity.state.value,
            city=entity.city,
            neighborhood=entity.neighborhood,
            street=entity.street,
            number=entity.number,
            complement=entity.complement,
            latitude=entity.latitude.value if entity.latitude else None,
            longitude=entity.longitude.value if entity.longitude else None,
            deleted_at=entity.deleted_at,
        )

    @staticmethod
    def update_model(model: AddressModel, entity: Address):
        model.id = entity.id
        model.zip_code = entity.zip_code.value
        model.country = entity.country.value
        model.state = entity.state.value
        model.city = entity.city
        model.neighborhood = entity.neighborhood
        model.street = entity.street
        model.number = entity.number
        model.complement = entity.complement
        model.latitude = entity.latitude.value if entity.latitude else None
        model.longitude = entity.longitude.value if entity.longitude else None
        model.deleted_at = entity.deleted_at

    @staticmethod
    def update_entity(target: Address, source: Address):
        target.id = source.id
        target.zip_code = source.zip_code
        target.country = source.country
        target.state = source.state
        target.city = source.city
        target.neighborhood = source.neighborhood
        target.street = source.street
        target.number = source.number
        target.complement = source.complement
        target.latitude = source.latitude
        target.longitude = source.longitude
        target.deleted_at = source.deleted_at
