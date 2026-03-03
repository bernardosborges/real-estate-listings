from __future__ import annotations
from datetime import datetime, timezone
from decimal import Decimal

from app.domain.value_objects.address.latitude import Latitude
from app.domain.value_objects.address.longitude import Longitude
from app.domain.value_objects.address.zipcode import ZipCode
from app.domain.enums.address_enum import CountryEnum, StateEnum
from app.domain.exceptions.address_exceptions import InvalidAddressField, InvalidAddressCoordinates
from app.domain.exceptions.domain_exception import AlreadyDeleted, CannotBeRestored, FieldTooLong
from app.domain.constants.address_constants import (
    ADDRESS_COMPLEMENT_MAX_LENGTH,
    ADDRESS_CITY_MAX_LENGTH,
    ADDRESS_NEIGHBORHOOD_MAX_LENGTH,
    ADDRESS_STREET_MAX_LENGTH,
    ADDRESS_NUMBER_MAX_LENGTH,
)


class Address:

    def __init__(
            self,
            id: int | None,
            zip_code: str,
            country: str,
            state: str,
            city: str,
            neighborhood: str | None,
            street: str,
            number: str,
            complement: str | None,
            latitude: Decimal | None,
            longitude: Decimal | None,
            deleted_at: datetime | None,
    ):

        self.id = id
        self.zip_code = ZipCode.from_raw(zip_code)
        self.country = CountryEnum.from_raw(country)
        self.state = StateEnum.from_raw(state)
        self.city = self._validate_text(city, ADDRESS_CITY_MAX_LENGTH, "city")
        self.neighborhood = self._validate_optional_text(neighborhood, ADDRESS_NEIGHBORHOOD_MAX_LENGTH, "neighborhood")
        self.street = self._validate_text(street, ADDRESS_STREET_MAX_LENGTH, "street")
        self.number = self._validate_text(number, ADDRESS_NUMBER_MAX_LENGTH, "number")
        self.complement = self._validate_optional_text(complement, ADDRESS_COMPLEMENT_MAX_LENGTH, "complement")
        self.deleted_at = deleted_at

        if latitude is None and longitude is None:
            self.latitude = None
            self.longitude = None
        elif latitude is not None and longitude is not None:
            self.latitude = Latitude.from_raw(latitude)
            self.longitude = Longitude.from_raw(longitude)
        else:
            raise InvalidAddressCoordinates()



# -----------------------------------------------
# LIFECYCLE
# -----------------------------------------------

    @property
    def is_deleted(self) -> bool:
        return self.deleted_at is not None


    def soft_delete(self) -> None:
        if self.is_deleted:
            raise AlreadyDeleted("address")
        self.deleted_at = datetime.now(timezone.utc)

    def restore(self) -> None:
        if self.deleted_at is None:
            raise CannotBeRestored("address")
        self.deleted_at = None


# -----------------------------------------------
# HELPERS
# -----------------------------------------------

    def update_basic_info(
            self,
            *,
            complement: str | None = None,
    ) -> None:
        if complement is not None:
            if len(complement) > ADDRESS_COMPLEMENT_MAX_LENGTH:
                raise FieldTooLong("complement")
            self.complement = complement

    def update_geocoding(
            self,
            *,
            latitude: Latitude | None,
            longitude: Longitude | None
    ) -> None:

        if (latitude is None) != (longitude is None):
            raise InvalidAddressCoordinates()

        self.latitude = latitude
        self.longitude =  longitude


    @staticmethod
    def _validate_text(value: str, max_length: int, field: str) -> str:
        if not value or not value.strip():
            raise InvalidAddressField(field)

        value = value.strip()

        if len(value) > max_length:
            raise FieldTooLong(field)

        return value


    @staticmethod
    def _validate_optional_text(value: str, max_length: int, field: str) -> str:
        if value is None:
            return None

        value = value.strip()

        if len(value) > max_length:
            raise FieldTooLong(field)

        return value
