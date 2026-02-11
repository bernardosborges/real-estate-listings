from abc import ABC, abstractmethod
from app.domain.entities.address import Address
from app.domain.value_objects.address.zipcode import ZipCode
from app.domain.enums.address_enum import CountryEnum, StateEnum

class AddressRepository(ABC):

    @abstractmethod
    def refresh(self, address: Address) -> Address:
        pass

    @abstractmethod
    def save(self, address: Address) -> Address:
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> Address | None:
        pass

    @abstractmethod
    def get_by_property_id(self, id: int) -> Address | None:
        pass

    @abstractmethod
    def get_by_full_address(self, zip_code: ZipCode, country: CountryEnum, state: StateEnum, city: str, neighborhood: str, street: str, number: str, complement: str | None = None) -> Address | None:
        pass