from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError



async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code = exc.status_code,
        content={"error": exc.detail, "path": str(request.url)}
    )

async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    return JSONResponse(
        status_code=500,
        content={"error": "Database error", "details": str(exc)}
    )

async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "details": str(exc)}
    )