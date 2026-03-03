from app.domain.entities.user import User
from app.domain.exceptions.user_profile_exceptions import UserProfileNotFound
from app.domain.exceptions.property_exceptions import PropertyNotFound, PropertyForbidden
from app.application.dto.property.update_property_input import UpdatePropertyInput
from app.application.dto.property.property_output import PropertyOutput
from app.application.unit_of_work.unit_of_work import UnitOfWork


class UpdatePropertyUseCase:

    """
    Use case responsible for updating a Property.
    """

    def __init__(
            self,
            uow: UnitOfWork
        ):

        self.uow = uow


    def execute(self, property_public_id: str, data: UpdatePropertyInput, current_user: User) -> None:

        # Check property
        db_property = self.uow.property_repository.get_by_public_id(property_public_id)
        if not db_property:
            raise PropertyNotFound()

        # Check profile
        db_profile = self.uow.profile_repository.get_by_user_id(current_user.id)
        if not db_profile:
            raise UserProfileNotFound(property_public_id)

        # Check ownership
        if db_property.profile_id != db_profile.id:
            raise PropertyForbidden()

        # Update entity
        db_property.update_basic_info(
            description = data.description,
            price = data.price,
            private_area = data.private_area
        )

        # Activate and persist all changes
        self.uow.property_repository.save(db_property)
        self.uow.commit()

        return PropertyOutput.from_entity(db_property, db_profile.public_id)
