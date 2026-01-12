from fastapi import Request
from fastapi.responses import JSONResponse
from app.core.exceptions.domain_exception import DomainException

async def domain_exception_handler(request: Request, exc: DomainException):
    return JSONResponse(status_code=exc.status_code, content={"error": exc.error_code, "message": exc.message})
