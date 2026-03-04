from __future__ import annotations
from decimal import Decimal
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
        zip_code: str,
        country: str,
        state: str,
        city: str,
        neighborhood: str | None,
        street: str,
        number: str,
        complement: str | None = None,
        latitude: Decimal | None = None,
        longitude: Decimal | None = None,
        deleted_at: datetime | None = None,
    ) -> Address:

        zip_code_vo = ZipCode.from_raw(zip_code)
        country_vo = CountryEnum.from_raw(country)
        state_vo = StateEnum.from_raw(state)

        latitude_vo = Latitude.from_raw(latitude) if latitude is not None else None
        longitude_vo = Longitude.from_raw(longitude) if longitude is not None else None

        return Address(
            id=None,
            zip_code=zip_code_vo,
            country=country_vo,
            state=state_vo,
            city=city,
            neighborhood=neighborhood,
            street=street,
            number=number,
            complement=complement,
            latitude=latitude_vo,
            longitude=longitude_vo,
            deleted_at=deleted_at,
        )
