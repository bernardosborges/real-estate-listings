from app.domain.entities.address import Address
from app.domain.repositories.address_repository import AddressRepository
from app.domain.value_objects.address.zipcode import ZipCode
from app.domain.enums.address_enum import CountryEnum, StateEnum


class FakeAddressRepository(AddressRepository):

    def __init__(self):
        self._addresses: list[Address] = []
        self._next_id = 1

    # -----------------------------------------------
    # PERSISTENCE
    # -----------------------------------------------

    def save(self, address: Address) -> Address:
        if address.id is None:
            address.id = self._next_id
            self._next_id += 1

        self._addresses = [a for a in self._addresses if a.id != address.id]

        self._addresses.append(address)
        return address

    def refresh(self, address: Address) -> Address:
        return self.get_by_id(address.id)

    # -----------------------------------------------
    # GETTERS
    # -----------------------------------------------

    def get_by_id(self, id: int) -> Address | None:
        for address in self._addresses:
            if address.id == id:
                return address
        return None

    def get_by_property_id(self, id: int) -> Address | None:
        for address in self._addresses:
            if address.property_id == id:
                return address
        return None

    def get_by_full_address(
        self,
        zip_code: ZipCode,
        country: CountryEnum,
        state: StateEnum,
        city: str,
        neighborhood: str,
        street: str,
        number: str,
        complement: str | None = None,
    ) -> Address | None:
        for address in self._addresses:
            if (
                address.zip_code == zip_code
                and address.country == country
                and address.state == state
                and address.city == city
                and address.neighborhood == neighborhood
                and address.street == street
                and address.number == number
                and address.complement == complement
            ):
                return address
        return None


# -----------------------------------------------
# LISTINGS
# -----------------------------------------------


# -----------------------------------------------
# STATE CHANGES
# -----------------------------------------------
