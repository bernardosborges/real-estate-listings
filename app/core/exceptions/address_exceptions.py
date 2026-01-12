from fastapi import status

from app.core.exceptions.domain_exception import DomainException


class CEPInvalid(DomainException):
    status_code = status.HTTP_400_BAD_REQUEST
    error_code = "ADDRESS_CEP_INVALID"
    message = "Invalid CEP format"

class CEPNotFound(DomainException):
    status_code = status.HTTP_404_NOT_FOUND
    error_code = "ADDRESS_CEP_NOT_FROUND"
    message = "CEP not found"

class AddressIncomplete(DomainException):
    status_code = status.HTTP_422_UNPROCESSABLE_CONTENT
    error_code = "ADDRESS_INCOMPLETE"
    message = "Address is missing required fields"
