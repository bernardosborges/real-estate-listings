from decimal import Decimal
from abc import ABC, abstractmethod
from app.domain.entities.property import Property
from app.domain.value_objects.property.property_public_id import PropertyPublicId
from app.domain.value_objects.user_profile.user_profile_public_id import UserProfilePublicId
from app.domain.value_objects.address.latitude import Latitude
from app.domain.value_objects.address.longitude import Longitude

class PropertyRepository(ABC):

    @abstractmethod
    def refresh(self, property: Property) -> Property:
        pass

    @abstractmethod
    def save(self, property: Property) -> Property:
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> Property | None:
        pass

    @abstractmethod
    def get_by_public_id(self, public_id: PropertyPublicId) -> Property | None:
        pass

    @abstractmethod
    def get_deleted_by_public_id(self, public_id: PropertyPublicId) -> Property | None:
        pass

    @abstractmethod
    def list_by_profile_id(self, profile_id: int, limit: int, offset: int, include_inactive: bool = False, price_min: Decimal | None = None, price_max: Decimal | None = None) -> list[Property]:
        pass

    @abstractmethod
    def list_for_map(self, lat_north: Latitude, lat_south: Latitude, lng_east: Longitude, lng_west: Longitude, limit: int, offset: int, include_inactive: bool = False, profile_id: int | None = None, price_min: Decimal | None = None, price_max: Decimal | None = None) -> list[Property]:
        pass

    @abstractmethod
    def exists_by_public_id(self, public_id: PropertyPublicId) -> bool:
        pass

    @abstractmethod
    def deactivate(self, id: int) -> None:
        pass

    @abstractmethod
    def activate(self, id: int) -> None:
        pass

    @abstractmethod
    def soft_delete(self, id: int) -> None:
        pass

    @abstractmethod
    def restore(self, id: int) -> None:
        pass
