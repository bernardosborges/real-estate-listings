import logging

from fastapi import Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger("app.infrastructure")


async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):

    logger.warning(
        "Database error",
        exc_info=True,
        extra={"method": request.method, "path": request.url.path},
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": {"code": "DATABASE_ERROR", "message": "An internal database error occurred."}},
    )
