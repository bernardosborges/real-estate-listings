from app.domain.entities.user import User
from app.domain.factories.property_factory import PropertyFactory
from app.domain.factories.address_factory import AddressFactory
from app.application.unit_of_work.unit_of_work import UnitOfWork
from app.domain.exceptions.user_profile_exceptions import UserProfileNotFound
from app.application.dto.property.property_output import PropertyOutput
from app.application.dto.property.create_property_input import CreatePropertyInput

from app.domain.value_objects.address.zipcode import ZipCode
from app.domain.enums.address_enum import CountryEnum
from app.domain.enums.address_enum import StateEnum


class CreatePropertyUseCase:

    """
    Use case responsible for creating a new Property for a Profile.
    """

    def __init__(
            self,
            uow: UnitOfWork
        ):

        self.uow = uow


    def execute(self, data: CreatePropertyInput, current_user: User) -> PropertyOutput:

        # Check profile
        db_profile = self.uow.profile_repository.get_by_user_id(current_user.id)
        if not db_profile:
            raise UserProfileNotFound("")

        # Conversion
        zipcode_vo = ZipCode.from_raw(data.address.zip_code)
        country_enum = CountryEnum.from_raw(data.address.country)
        state_enum = StateEnum.from_raw(data.address.state)

        # Check address
        db_address = self.uow.address_repository.get_by_full_address(
            zip_code = zipcode_vo,
            country = country_enum,
            state = state_enum,
            city = data.address.city,
            neighborhood = data.address.neighborhood,
            street = data.address.street,
            number = data.address.number,
            complement = data.address.complement
        )

        if db_address is None:
            db_address = AddressFactory.create(
                zip_code = data.address.zip_code,
                country = data.address.country,
                state = data.address.state,
                city = data.address.city,
                neighborhood = data.address.neighborhood,
                street = data.address.street,
                number = data.address.number,
                complement = data.address.complement,
                latitude = data.address.latitude,
                longitude = data.address.longitude
            )
            self.uow.address_repository.save(db_address)

        # Create the property entity
        property_entity = PropertyFactory.create_for_profile(
            profile_id = db_profile.id,
            address = db_address,
            description = data.description,
            price = data.price,
            private_area = data.private_area
        )
        self.uow.property_repository.save(property_entity)

        # Persist all changes (user and profile) and refresh the entity state
        self.uow.commit()

        # Convert the domain entity to output DTO and return
        return PropertyOutput.from_entity(property_entity, db_profile.public_id)
