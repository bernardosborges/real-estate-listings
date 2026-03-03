from fastapi import FastAPI, HTTPException
from sqlalchemy.exc import SQLAlchemyError

from app.core.logging import setup_logging
from app.api.routers import addresses_router, auth_router, property_router
# from app.api.routers import property_router, auth_router, zipcode_router,
# tag_group_router, tag_router, property_tag_router, photo_router, user_profile_router

from app.api.exception_handlers.domain_exception_handler import domain_exception_handler
from app.api.exception_handlers.api_exception_handler import api_exception_handler
from app.api.exception_handlers.sqlalchemy_exception_handler import sqlalchemy_exception_handler
from app.api.exception_handlers.http_exception_handler import http_exception_handler
from app.api.exception_handlers.unhandled_exception_handler import unhandled_exception_handler

from app.domain.exceptions.domain_exception import DomainException
from app.api.exceptions.api_exception import APIException


setup_logging()

app = FastAPI(
    title="Real Estate Listing API",
    version="0.1.0"
)

app.include_router(property_router.router)
app.include_router(auth_router.router)
app.include_router(addresses_router.router)
#app.include_router(tag_group_router.router)
#app.include_router(tag_router.router)
#app.include_router(property_tag_router.router)
#app.include_router(photo_router.router)
#app.include_router(user_profile_router.router)

# Register global exceptions handlers
app.add_exception_handler(DomainException, domain_exception_handler)
app.add_exception_handler(APIException, api_exception_handler)
app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)

@app.get("/")
def healthcheck():
    return {"status": "ok"}
