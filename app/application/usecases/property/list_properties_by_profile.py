from decimal import Decimal

from app.domain.entities.user import User
from app.application.unit_of_work.unit_of_work import UnitOfWork
from app.domain.exceptions.user_profile_exceptions import UserProfileNotFound
from app.application.dto.property.property_list_output import PropertyListOutput


class ListPropertiesByProfileUseCase:

    """
    Use case responsible for creating a new Property for a Profile.
    """

    def __init__(
            self,
            uow: UnitOfWork
        ):

        self.uow = uow


    def execute(self, profile_public_id: str, current_user: User, limit: int = 20, offset: int = 0, price_min: Decimal | None = None, price_max: Decimal | None = None) -> list[PropertyListOutput]:

        # Check profile
        db_profile = self.uow.profile_repository.get_by_public_id(profile_public_id)
        if not db_profile:
            raise UserProfileNotFound()
        
        # Check if user is owner of profile
        include_inactive = current_user is not None and db_profile.user_id == current_user.id

        # List properties
        db_properties = self.uow.property_repository.list_by_profile_id(
            profile_id = db_profile.id,
            limit = limit,
            offset = offset,
            include_inactive = include_inactive,
            price_min = price_min,
            price_max = price_max
        )

        # Returned mapped
        properties_output = [
            PropertyListOutput.from_entity(property, db_profile.public_id)
            for property in db_properties
        ]
        return properties_output