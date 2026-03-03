from abc import ABC, abstractmethod

from app.application.services.geocoding_result import GeocodingResult

class GeocodingService(ABC):

    @abstractmethod
    async def geocode(
        self,
        *,
        zip_code: str,
        country: str,
        state: str,
        city: str,
        neighborhood: str | None,
        street: str,
        number: str
    ) -> GeocodingResult | None:
        """
        Returns:
            GeocodingResult: if found
            None: if no result
        Raises:
            GeocodingUnavailable
        """
        pass
