from decimal import Decimal


class AddressOutput:

    def __init__(
            self,
            zip_code: str,
            country: str,
            state: str,
            city: str,
            neighborhood: str,
            street: str,
            number: str,
            complement: str | None = None,
            latitude: Decimal | None = None,
            longitude: Decimal | None = None,
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


    @classmethod
    def from_entity(cls, address):
        return cls(
            zip_code = address.zip_code.value,
            country = address.country.value,
            state = address.state.value,
            city = address.city,
            neighborhood = address.neighborhood,
            street = address.street,
            number = address.number,
            complement = address.complement,
            latitude = address.latitude.value if address.latitude else None,
            longitude = address.longitude.value if address.longitude else None,
        )