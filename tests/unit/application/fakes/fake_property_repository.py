from decimal import Decimal

from app.domain.entities.property import Property
from app.domain.repositories.property_repository import PropertyRepository
from app.domain.value_objects.property.property_public_id import PropertyPublicId
from app.domain.value_objects.address.latitude import Latitude
from app.domain.value_objects.address.longitude import Longitude


class FakePropertyRepository(PropertyRepository):

    def __init__(self):
        self._properties: list[Property] = []
        self._next_id = 1

    # -----------------------------------------------
    # PERSISTENCE
    # -----------------------------------------------

    def save(self, property: Property) -> Property:
        if property.id is None:
            property.id = self._next_id
            self._next_id += 1

        self._properties = [p for p in self._properties if p.id != property.id]

        self._properties.append(property)
        return property

    def refresh(self, property: Property) -> Property:
        return self.get_by_id(property.id)

    # -----------------------------------------------
    # GETTERS
    # -----------------------------------------------

    def get_by_id(self, id: int) -> Property | None:
        for property in self._properties:
            if property.id == id:
                return property
        return None

    def get_by_public_id(self, public_id: PropertyPublicId) -> Property | None:
        for property in self._properties:
            if property.public_id == public_id and not property.is_deleted:
                return property
        return None

    def get_deleted_by_public_id(self, public_id: PropertyPublicId) -> Property | None:
        for property in self._properties:
            if property.public_id == public_id and property.is_deleted:
                return property
        return None

    def exists_by_public_id(self, public_id: PropertyPublicId) -> bool:
        return any(p.public_id == public_id for p in self._properties)

    # -----------------------------------------------
    # LISTINGS
    # -----------------------------------------------

    def list_by_profile_id(
        self,
        profile_id: int,
        limit: int,
        offset: int,
        include_inactive: bool = False,
        price_min: Decimal | None = None,
        price_max: Decimal | None = None,
    ) -> list[Property]:
        result = [
            p
            for p in self._properties
            if p.profile_id == profile_id
            and not p.is_deleted
            and (include_inactive or p.is_active)
            and (price_min is None or p.price.value >= price_min)
            and (price_max is None or p.price.value <= price_max)
        ]
        return result[offset : offset + limit]

    def list_for_map(
        self,
        lat_north: Latitude,
        lat_south: Latitude,
        lng_east: Longitude,
        lng_west: Longitude,
        limit: int,
        offset: int,
        include_inactive: bool = False,
        profile_id: int | None = None,
        price_min: Decimal | None = None,
        price_max: Decimal | None = None,
    ) -> list[Property]:
        result = [
            p
            for p in self._properties
            if not p.is_deleted
            and (include_inactive or p.is_active)
            and (profile_id is None and p.profile_id == profile_id)
            and (price_min is None or p.price.value >= price_min)
            and (price_max is None or p.price.value <= price_max)
            and p.address.latitude is not None
            and p.address.longitude is not None
            and lat_south.value <= p.address.latitude.value <= lat_north.value
            and lng_west.value <= p.address.longitude.value <= lng_east.value
        ]
        return result[offset : offset + limit]

    # -----------------------------------------------
    # STATE CHANGES
    # -----------------------------------------------

    def deactivate(self, id: int) -> None:
        property = self.get_by_id(id)
        if property:
            property.deactivate()

    def activate(self, id: int) -> None:
        property = self.get_by_id(id)
        if property:
            property.activate()

    def soft_delete(self, id: int) -> None:
        property = self.get_by_id(id)
        if property:
            property.soft_delete()

    def restore(self, id: int) -> None:
        property = self.get_by_id(id)
        if property:
            property.restore()
