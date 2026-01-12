import httpx
import logging

from fastapi import HTTPException, status
from decimal import Decimal

from app.core.config import settings
from app.schemas.address_schema import AddressCreateSchema
from app.core.exceptions.geocoding_exceptions import GeocodingFailed, GeocodingUnavailable

GOOGLE_GEOCODE_URL = "https://maps.googleapis.com/maps/api/geocode/json"
logger = logging.getLogger(__name__)

async def geocode_address (address: AddressCreateSchema) -> tuple[Decimal, Decimal]:

    full_address = build_full_address(address)

    params = {
        "address": full_address,
        "key": settings.GOOGLE_CODING_API_KEY
    }

    #logger.info("Geocoding address",extra={"zip_code": address.zip_code,"street": address.street,"city": address.city,"state": address.state,})

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(GOOGLE_GEOCODE_URL, params=params)
    except httpx.RequestError as exc:
        logger.warning("Geocoding service unavailable", extra={"address": full_address, "error": str(exc)})
        raise GeocodingUnavailable()
    except httpx.HTTPStatusError:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Error communicating with geocoding service")
    
    if response.status_code != 200:
        logger.error("Invalid response from geocoding provider", extra={"status_code": response.status_code, "body": response.text})
        raise GeocodingUnavailable()

    data = response.json()
    print("GOOGLE GEOCODING RESPONSE:", data)

    if data.get("status") != "OK" or not data.get("results"):
        logger.info("Geocoding failed", extra={"address": full_address, "provider_status": data.get("status")})
        raise GeocodingFailed()

    location = data["results"][0]["geometry"]["location"]

    return (
        Decimal(str(location["lat"])),
        Decimal(str(location["lng"]))
    )

def build_full_address(address: AddressCreateSchema) -> str:
    parts = [
        address.street,
        address.number,
        address.neighborhood,
        address.city,
        address.state,
        address.zip_code,
        address.country
    ]

    clean_parts = [str(p) for p in parts if p]

    return ", ".join(clean_parts)