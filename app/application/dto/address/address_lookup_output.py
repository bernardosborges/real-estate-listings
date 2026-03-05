from app.domain.value_objects.address.zipcode import ZipCode
from app.domain.enums.address_enum import CountryEnum, StateEnum


class AddressLookupOutput:

    def __init__(
        self,
        zip_code: ZipCode,
        country: CountryEnum,
        state: StateEnum,
        city: str,
        neighborhood: str | None = None,
        street: str | None = None,
    ):
        self.zip_code = zip_code
        self.country = country
        self.state = state
        self.city = city
        self.neighborhood = neighborhood
        self.street = street
