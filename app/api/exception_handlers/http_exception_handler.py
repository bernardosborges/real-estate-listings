import logging

from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse


logger = logging.getLogger("app.http")

async def http_exception_handler(request: Request, exc: HTTPException):

    logger.warning(
        "HTTP error",
        exc_info=True,
        extra = {
            "error_code": exc.status_code,
            "error_message": exc.detail,
            "method": request.method,
            "path": request.url.path
        },
    )

    return JSONResponse(
        status_code = exc.status_code,
        content = {
            "error": {
                "code": "HTTP_ERROR",
                "message": exc.detail
            }
        }
    )