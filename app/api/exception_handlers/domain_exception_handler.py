from fastapi import Request, status
from fastapi.responses import JSONResponse
import logging

from app.domain.exceptions.domain_exception import DomainException
from app.api.exception_handlers.error_mapping import DOMAIN_ERROR_HTTP_MAP

logger = logging.getLogger("app.domain")

async def domain_exception_handler(request: Request, exc: DomainException):

    status_code = DOMAIN_ERROR_HTTP_MAP.get(
        exc.error_code,
        status.HTTP_400_BAD_REQUEST,
    ) 

    logger.warning(
        "Domain error",
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

