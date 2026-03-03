import logging
from fastapi import Request, status
from fastapi.responses import JSONResponse


from app.api.exceptions.api_exception import APIException
from app.api.exception_handlers.error_mapping import API_ERROR_HTTP_MAP


logger = logging.getLogger("app.api")

async def api_exception_handler(request: Request, exc: APIException):

    status_code = API_ERROR_HTTP_MAP.get(
        exc.error_code,
        status.HTTP_400_BAD_REQUEST,
    )

    logger.warning(
        "API error",
        extra = {
            "error_code": exc.error_code,
            "error_message": exc.message,
            "context": exc.context,
            "method": request.method,
            "path": request.url.path
        },
    )

    return JSONResponse(
        status_code = status_code,
        content = {
            "error": {
                "code": exc.error_code,
                "message": exc.message
            }
        }
    )
