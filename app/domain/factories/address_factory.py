from __future__ import annotations
from datetime import datetime

from app.domain.entities.address import Address
from app.domain.value_objects.address.latitude import Latitude
from app.domain.value_objects.address.longitude import Longitude
from app.domain.value_objects.address.zipcode import ZipCode
from app.domain.enums.address_enum import CountryEnum, StateEnum


class AddressFactory:

    @classmethod
    def create(
        cls,
        *,
        zip_code: ZipCode,
        country: CountryEnum,
        state: StateEnum,
        city: str,
        neighborhood: str | None,
        street: str,
        number: str,
        complement: str | None = None,
        latitude: Latitude | None = None,
        longitude: Longitude | None = None,
        deleted_at: datetime | None = None,
    ) -> Address:

        return Address(
            id = None,
            zip_code = zip_code,
            country = country,
            state = state,
            city = city,
            neighborhood = neighborhood,
            street = street,
            number = number,
            complement = complement,
            latitude = latitude,
            longitude = longitude,
            deleted_at = deleted_at
        )
