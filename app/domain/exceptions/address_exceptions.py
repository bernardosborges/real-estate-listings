from app.domain.exceptions.domain_exception import DomainException

class InvalidLatitude(DomainException):
    error_code = "INVALID_LATITUDE"
    message = "Invalid latitude."

    def __init__(self, value: str):
        super().__init__(
            message = f"Invalid latitude: '{value}'.",
            value = value
        )

class InvalidLongitude(DomainException):
    error_code = "INVALID_LONGITUDE"
    message = "Invalid longitude."

    def __init__(self, value: str):
        super().__init__(
            message = f"Invalid longitude: '{value}'.",
            value = value
        )

class InvalidZipCode(DomainException):
    error_code = "INVALID_ZIPCODE"
    message = "Invalid ZipCode."

    def __init__(self, value: str):
        super().__init__(
            message = f"Invalid zipcode: '{value}'.",
            value = value
        )

class InvalidAddressField(DomainException):
    error_code = "INVALID_ADDRESS_FIELD"
    message = "Invalid address field."

    def __init__(self, value: str):
        super().__init__(
            message = f"Invalid address field: '{value}'.",
            value = value
        )
    
class InvalidAddressCoordinates(DomainException):
    error_code = "INVALID_ADDRESS_COORDINATES"
    message = "Invalid address coordinates."


class CEPInvalid(DomainException):
    error_code = "ADDRESS_CEP_INVALID"
    message = "Invalid CEP format"


class CEPNotFound(DomainException):
    error_code = "ADDRESS_CEP_NOT_FOUND"
    message = "CEP was not found"

    def __init__(self, cep: str | None = None):
        super().__init__(
            message = f"CEP '{cep}' was not found",
            cep = cep
        )


class AddressIncomplete(DomainException):
    error_code = "ADDRESS_INCOMPLETE"
    message = "Address is missing required fields"


class AddressNotFound(DomainException):
    error_code = "ADDRESS_NOT_FOUND"
    message = "Address was not found"

class AddressLookUpFailed(DomainException):
    error_code = "ADDRESS_LOOKUP_FAILED"
    message = "Address lookup failed."

class InvalidState(DomainException):
    error_code = "INVALID_UF_STATE"
    message = "Invalid UF State."

class InvalidCountry(DomainException):
    error_code = "INVALID_COUNTRY"
    message = "Invalid country."