from app.application.exceptions.application_exception import ApplicationException



class GeocodingUnavailable(ApplicationException):
    error_code = "GEOCODING_UNAVAILABLE"
    message = "Geocoding service unavailable."


class GeocodingFailed(ApplicationException):
    error_code = "GEOCODING_FAILED"
    message = "Unable to geocode address."

class AddressNotFound(ApplicationException):
    error_code = "ADDRESS_NOT_FOUND"
    message = "Unable to find geocode for this address."   