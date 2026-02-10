from app.application.services.address_lookup_service import AddressLookupService
from app.application.dto.address.address_lookup_output import AddressLookupOutput
from app.domain.value_objects.address.zipcode import ZipCode

class LookupAddressByZipCodeUseCase:

    def __init__(self, address_lookup_service: AddressLookupService):
        self.address_lookup_service = address_lookup_service

    async def execute(self, *, zip_code: str) -> AddressLookupOutput:

        zipcode_vo = ZipCode.from_raw(zip_code)

        result = await self.address_lookup_service.lookup_by_zipcode(zipcode_vo)

        return result