from fastapi import status
from app.core.exceptions.domain_exception import DomainException


class GeocodingUnavailable(DomainException):
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    error_code = "GEOCODING_UNAVAILABLE"
    message = "Geocoding service unavailable"


class GeocodingFailed(DomainException):
    status_code = status.HTTP_422_UNPROCESSABLE_CONTENT
    error_code = "GEOCODING_FAILED"
    message = "Unable to geocode address"
