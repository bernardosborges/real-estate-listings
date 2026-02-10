import httpx

from app.application.services.address_lookup_service import AddressLookupService
from app.domain.value_objects.address.zipcode import ZipCode
from app.domain.enums.address_enum import CountryEnum, StateEnum
from app.application.services.address_lookup_result import AddressLookupResult
from app.domain.exceptions.address_exceptions import CEPNotFound, AddressLookUpFailed

class ViaCEPService(AddressLookupService):

    BASE_URL = "https://viacep.com.br/ws/"

    async def lookup_by_zipcode(self, zip_code: ZipCode) -> AddressLookupResult:

        url = f"{self.BASE_URL}/{str(zip_code)}/json/"
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(url)
        except httpx.RequestError as exc:
            raise AddressLookUpFailed("Failed to connect to ViaCEP.") from exc

        if response.status_code != 200:
            raise CEPNotFound()

        data = response.json()

        if data.get("erro") is True:
            raise CEPNotFound(f"Zip code not found: {zip_code}")

        return AddressLookupResult(
            zip_code = zip_code,
            country = CountryEnum.BR,
            state = StateEnum.from_raw(data["uf"]),
            city = data.get("localidade"),
            neighborhood = data.get("bairro"),
            street = data.get("logradouro"),
        )