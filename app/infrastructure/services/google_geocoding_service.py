import httpx
import logging

from decimal import Decimal

from app.core.config import settings
from app.application.services.geocoding_service import GeocodingService
from app.application.services.geocoding_result import GeocodingResult
from app.application.exceptions.geocoding_exceptions import (
    GeocodingFailed,
    GeocodingUnavailable,
)

GOOGLE_GEOCODE_URL = "https://maps.googleapis.com/maps/api/geocode/json"
logger = logging.getLogger(__name__)


class GoogleGeocodingService(GeocodingService):

    PROVIDER_NAME = "google"

    HTTP_TIMEOUT_SECONDS = 5.0

    LOCATION_TYPE_CONFIDENCE = {
        "ROOFTOP": 1.0,
        "RANGE_INTERPOLATED": 0.8,
        "GEOMETRIC_CENTER": 0.6,
        "APPROXIMATE": 0.4,
    }

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

        full_address = ", ".join(
            filter(None, [street, number, neighborhood, city, state, zip_code, country])
        )

        params = {"address": full_address, "key": settings.GOOGLE_CODING_API_KEY}

        try:
            async with httpx.AsyncClient(timeout=self.HTTP_TIMEOUT_SECONDS) as client:
                response = await client.get(GOOGLE_GEOCODE_URL, params=params)
        except httpx.RequestError as exc:
            logger.warning(
                "Geocoding provider unavailable",
                extra={"error": str(exc), "address": full_address},
            )
            raise GeocodingUnavailable()

        if response.status_code != 200:
            logger.error(
                "Invalid response from geocoding provider",
                extra={
                    "status_code": response.status_code,
                    "body": response.text,
                    "address": full_address,
                },
            )
            raise GeocodingUnavailable()

        data = response.json()
        status = data.get("status")
        results = data.get("results")

        if status == "ZERO_RESULTS" or not results:
            logger.info(
                "Geocoding returned no results",
                extra={"address": full_address, "provider_status": status},
            )
            return None

        if status != "OK":
            logger.error(
                "Unexpected geocoding provider status",
                extra={"address": full_address, "provider_status": status},
            )
            raise GeocodingFailed()

        geometry = results[0].get("geometry")
        if not geometry:
            logger.error(
                "Missing geometry in geocoding provider status",
                extra={"address": full_address, "result": results[0]},
            )
            raise GeocodingFailed()

        location = geometry.get("location")
        location_type = geometry.get("location_type")

        if not location or "lat" not in location or "lng" not in location:
            logger.error(
                "Invalid location payload from geocoding provider",
                extra={"address": full_address, "geometry": geometry},
            )
            raise GeocodingFailed()

        confidence = self.LOCATION_TYPE_CONFIDENCE.get(location_type, 0.0)

        return GeocodingResult(
            latitude=Decimal(str(location["lat"])),
            longitude=Decimal(str(location["lng"])),
            confidence=confidence,
            provider=self.PROVIDER_NAME,
        )
