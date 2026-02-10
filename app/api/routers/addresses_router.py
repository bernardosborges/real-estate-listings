from fastapi import APIRouter, Depends

from app.api.deps.oauth2 import get_current_user
from app.api.deps.address_deps import get_address_lookup_service, get_geocoding_service
from app.api.schemas.address.address_schema import LookupAddressResponseSchema
from app.api.schemas.address.geocoding_schema import GeolocationPreviewRequestSchema, GeolocationPreviewResponseSchema
from app.application.usecases.address.lookup_address_by_zipcode import LookupAddressByZipCodeUseCase
from app.application.usecases.address.lookup_address_geolocation_preview import LookupAddressGeolocationPreviewUseCase
from app.application.services.address_lookup_service import AddressLookupService
from app.application.services.geocoding_service import GeocodingService
from app.application.dto.address.address_geolocation_preview_input import AddressGeolocationPreviewInput
from app.domain.entities.user import User
from app.core.config import settings

router = APIRouter(prefix=f"{settings.API_PREFIX}/addresses", tags=["Addresses"])


# -----------------------------------------------
# ENDPOINT - GET CEP
# -----------------------------------------------

@router.get(
        "/cep/{zip_code}",
        response_model=LookupAddressResponseSchema,
        summary="Get address from a CEP",
        description="Returns address data from ViaCEP (authenticated users only)"
)
async def lookup_cep_endpoint(
    zip_code: str,
    current_user: User = Depends(get_current_user),
    address_lookup_service: AddressLookupService = Depends(get_address_lookup_service)
):

    lookup_usecase = LookupAddressByZipCodeUseCase(address_lookup_service)
    result = await lookup_usecase.execute(zip_code=zip_code)

    return LookupAddressResponseSchema(
        zip_code = result.zip_code.formatted,
        country = result.country.value,
        state = result.state.value,
        city = result.city,
        neighborhood = result.neighborhood,
        street = result.street,
    )

# -----------------------------------------------
# ENDPOINT - GET GEOCODING
# -----------------------------------------------

@router.get(
        "/geolocation/preview",
        response_model=GeolocationPreviewResponseSchema,
        summary="Get geocoding for an address",
        description="Returns geocode from Google (authenticated users only)"
)
async def lookup_geolocation_preview_endpoint(
    payload: GeolocationPreviewRequestSchema,
    current_user: User = Depends(get_current_user),
    address_geocoding_service: GeocodingService = Depends(get_geocoding_service)
):

    lookup_usecase = LookupAddressGeolocationPreviewUseCase(address_geocoding_service)

    usecase_input = AddressGeolocationPreviewInput(
        zip_code = payload.zip_code,
        country = payload.country,
        state = payload.state,
        city = payload.city,
        neighborhood = payload.neighborhood,
        street = payload.street,
        number = payload.number
    )

    result = await lookup_usecase.execute(usecase_input)

    return GeolocationPreviewResponseSchema(
            latitude = result.latitude,
            longitude = result.longitude,
            confidence = result.confidence,
            provider = result.provider
        )