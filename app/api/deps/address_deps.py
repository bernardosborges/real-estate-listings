from app.application.services.address_lookup_service import AddressLookupService
from app.application.services.geocoding_service import GeocodingService
from app.infrastructure.services.viacep_service import ViaCEPService
from app.infrastructure.services.google_geocoding_service import GoogleGeocodingService

def get_address_lookup_service() -> AddressLookupService:
    return ViaCEPService()

def get_geocoding_service() -> GeocodingService:
    return GoogleGeocodingService()
