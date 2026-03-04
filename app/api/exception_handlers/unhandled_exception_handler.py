import logging

from fastapi import Request, status
from fastapi.responses import JSONResponse

logger = logging.getLogger("app.infrastructure")


async def unhandled_exception_handler(request: Request, exc: Exception):

    logger.warning(
        "Unhandled exception",
        exc_info=True,
        extra={"method": request.method, "path": request.url.path},
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": {"code": "INTERNAL_SERVER_ERROR", "message": "An unexpected error occurred."}},
    )
