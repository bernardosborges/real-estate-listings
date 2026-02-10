from decimal import Decimal

from app.domain.entities.address import Address
from app.domain.factories.address_factory import AddressFactory
from app.domain.value_objects.address.zipcode import ZipCode
from app.domain.value_objects.address.latitude import Latitude
from app.domain.value_objects.address.longitude import Longitude
from app.domain.enums.address_enum import CountryEnum, StateEnum


class AddressInput:

    def __init__(
            self,
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
            confidence: float | None = None,
            provider: str | None = None
    ):
        self.zip_code = zip_code
        self.country = country
        self.state = state
        self.city = city
        self.neighborhood = neighborhood
        self.street = street
        self.number = number
        self.complement = complement
        self.latitude = latitude
        self.longitude = longitude
        self.confidence = confidence
        self.provider = provider

    # def to_entity(self) -> Address:
    #     return AddressFactory.create(
    #         zip_code = ZipCode.from_raw(self.zip_code), 
    #         country = CountryEnum.from_raw(self.country), 
    #         state = StateEnum.from_raw(self.state), 
    #         city = self.city, 
    #         neighborhood = self.neighborhood, 
    #         street = self.street, 
    #         number = self.number, 
    #         complement = self.complement, 
    #         latitude = Latitude.from_raw(self.latitude),
    #         longitude = Longitude.from_raw(self.longitude),
    #         deleted_at = None
    #     )
