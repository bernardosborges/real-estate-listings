from decimal import Decimal

from app.domain.entities.user import User
from app.application.unit_of_work.unit_of_work import UnitOfWork
from app.domain.exceptions.user_profile_exceptions import UserProfileNotFound
from app.domain.value_objects.address.latitude import Latitude
from app.domain.value_objects.address.longitude import Longitude
from app.application.dto.property.property_list_output import PropertyListOutput
from app.application.dto.property.list_for_map_property_input import ListForMapPropertyInput


class ListPropertiesForMapUseCase:

    """
    Use case responsible for creating a new Property for a Profile.
    """

    def __init__(
            self,
            uow: UnitOfWork
        ):

        self.uow = uow


    def execute(
            self,
            data: ListForMapPropertyInput,
            current_user: User,
            limit: int = 20,
            offset: int = 0,
            price_min: Decimal | None = None,
            price_max: Decimal | None = None,
        ) -> list[PropertyListOutput]:

        # Validate map limits
        normalized_lat_north = Latitude.from_raw(data.lat_north)
        normalized_lat_south = Latitude.from_raw(data.lat_south)
        normalized_lng_east = Longitude.from_raw(data.lng_east)
        normalized_lng_west = Longitude.from_raw(data.lng_west)

        # Check profile
        db_profile = None
        if data.profile_public_id:
            db_profile = self.uow.profile_repository.get_by_public_id(data.profile_public_id)
            if not db_profile:
                raise UserProfileNotFound()
        
        # Check if user is owner of profile
        include_inactive = current_user is not None and db_profile is not None and db_profile.user_id == current_user.id

        # List properties
        db_properties = self.uow.property_repository.list_for_map(
            lat_north = normalized_lat_north,
            lat_south = normalized_lat_south,
            lng_east = normalized_lng_east,
            lng_west = normalized_lng_west,
            limit = limit,
            offset = offset,
            include_inactive = include_inactive,
            profile_id = db_profile.id if db_profile else None,
            price_min = price_min,
            price_max = price_max
        )

        # Returned mapped
        properties_output = [
            PropertyListOutput.from_entity(
                property,
                db_profile.public_id if db_profile else None
            )
            for property in db_properties
        ]
        return properties_output