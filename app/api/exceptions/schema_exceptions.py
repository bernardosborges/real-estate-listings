from app.api.exceptions.api_exception import APIException


class InvalidPriceFilters(APIException):
    error_code = "INVALID_PRICE_FILTERS"
    message = "Maximum price cannot be less than minimum price."


class InvalidMapBounds(APIException):
    error_code = "INVALID_MAP_BOUNDS"
    message = "Latitude north must be greater than south and longitude east must be greater than west."