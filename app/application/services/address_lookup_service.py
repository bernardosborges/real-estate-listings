from abc import ABC, abstractmethod
from app.domain.value_objects.address.zipcode import ZipCode
from app.application.services.address_lookup_result import AddressLookupResult

class AddressLookupService(ABC):

    @abstractmethod
    async def lookup_by_zipcode(self, zip_code: ZipCode) -> AddressLookupResult:
        pass