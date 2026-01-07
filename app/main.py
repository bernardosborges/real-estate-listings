from fastapi import FastAPI,HTTPException
from app.routers import property_router
from app.core import exceptions
from sqlalchemy.exc import SQLAlchemyError

app = FastAPI(
    title="Real Estate Listing API",
    version="0.1.0"
)

API_PREFIX = "/api/v0"
app.include_router(property_router.router, prefix=API_PREFIX)

# Register global exceptions handlers
app.add_exception_handler(HTTPException, exceptions.http_exception_handler)
app.add_exception_handler(Exception, exceptions.generic_exception_handler)
app.add_exception_handler(SQLAlchemyError, exceptions.sqlalchemy_exception_handler)

@app.get("/")
def healthcheck():
    return {"status": "ok"}