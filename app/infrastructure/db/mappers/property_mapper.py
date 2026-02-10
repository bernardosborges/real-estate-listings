from app.domain.entities.property import Property
from app.infrastructure.db.models.property_model import PropertyModel
from app.infrastructure.db.mappers.address_mapper import AddressMapper
from app.domain.value_objects.property.price import Price
from app.domain.value_objects.property.private_area import PrivateArea
from app.domain.value_objects.property.property_public_id import PropertyPublicId



class PropertyMapper:

    @staticmethod
    def to_entity(model: PropertyModel) -> Property:

        address_entity = None
        if model.address:
            address_entity = AddressMapper.to_entity(model.address)

        return Property(
            id = model.id,
            public_id = model.public_id,
            profile_id = model.profile_id,
            address = address_entity,
            description = model.description,
            price = model.price,
            private_area = model.private_area,
            is_active = model.is_active,
            deleted_at = model.deleted_at,
        )


    @staticmethod
    def to_model(entity: Property) -> PropertyModel:
        model = PropertyModel(
            id = entity.id,
            public_id = entity.public_id,
            profile_id = entity.profile_id,
            description = entity.description,
            price = entity.price.value,
            private_area = entity.private_area.value,
            is_active = entity.is_active,
            deleted_at = entity.deleted_at,
        )
        if entity.address and entity.address.id:
            model.address_id = entity.address.id
            #model.address = AddressMapper.to_model(entity.address)

        return model

    @staticmethod
    def update_model(model: PropertyModel, entity: Property):
        model.id = entity.id
        model.public_id = entity.public_id
        model.profile_id = entity.profile_id
        model.address_id = entity.address.id
        model.description = entity.description
        model.price = entity.price.value
        model.private_area = entity.private_area.value
        model.is_active = entity.is_active
        model.deleted_at = entity.deleted_at

        if entity.address:
            if model.address:
                AddressMapper.update_model(model.address, entity.address)
            else:
                model.address = AddressMapper.to_model(entity.address)


    @staticmethod
    def update_entity(target: Property, source: Property) -> Property:
        target.id = source.id
        target.public_id = source.public_id
        target.profile_id = source.profile_id
        target.address = source.address
        target.description = source.description
        target.price = source.price
        target.private_area = source.private_area
        target.is_active = source.is_active
        target.deleted_at = source.deleted_at