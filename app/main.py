from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from app.core.exceptions import domain_exception
from app.routers import property_router, auth_router, zipcode_router, tag_group_router, tag_router, property_tag_router
from app.core.exceptions.domain_exception import DomainException
from app.core.exceptions import exception_handlers
from app.core.exceptions.domain_exception import PropertyForbidden, PropertyNotFound

app = FastAPI(
    title="Real Estate Listing API",
    version="0.1.0"
)

app.include_router(property_router.router)
app.include_router(auth_router.router)
app.include_router(zipcode_router.router)
app.include_router(tag_group_router.router)
app.include_router(tag_router.router)
app.include_router(property_tag_router.router)

# # Register global exceptions handlers
# app.add_exception_handler(HTTPException, exception.http_exception_handler)
# app.add_exception_handler(Exception, exception.generic_exception_handler)
# app.add_exception_handler(SQLAlchemyError, exception.sqlalchemy_exception_handler)

app.add_exception_handler(DomainException, exception_handlers.domain_exception_handler)

@app.get("/")
def healthcheck():
    return {"status": "ok"}