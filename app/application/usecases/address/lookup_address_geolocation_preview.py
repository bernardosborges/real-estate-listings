from app.application.services.geocoding_service import GeocodingService
from app.application.dto.address.address_geolocation_preview_input import AddressGeolocationPreviewInput
from app.application.dto.address.address_geolocation_preview_output import AddressGeolocationPreviewOutput
from app.application.exceptions.geocoding_exceptions import AddressNotFound

class LookupAddressGeolocationPreviewUseCase:


    def __init__(self, geocoding_service: GeocodingService):
        self.geocoding_service = geocoding_service

    async def execute(
            self,
            data: AddressGeolocationPreviewInput
    ) -> AddressGeolocationPreviewOutput:

        result = await self.geocoding_service.geocode(
                    zip_code = data.zip_code,
                    country = data.country,
                    state = data.state,
                    city = data.city,
                    neighborhood = data.neighborhood,
                    street = data.street,
                    number = data.number
                )

        if result is None:
            raise AddressNotFound()

        return AddressGeolocationPreviewOutput(
            latitude = result.latitude,
            longitude = result.longitude,
            confidence = result.confidence,
            provider = result.provider
        )
