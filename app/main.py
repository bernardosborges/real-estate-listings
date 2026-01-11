from fastapi import FastAPI,HTTPException
from sqlalchemy.exc import SQLAlchemyError
from app.core import exceptions
from app.routers import property_router, auth_router, zipcode_router


app = FastAPI(
    title="Real Estate Listing API",
    version="0.1.0"
)

app.include_router(property_router.router)
app.include_router(auth_router.router)
app.include_router(zipcode_router.router)

# Register global exceptions handlers
app.add_exception_handler(HTTPException, exceptions.http_exception_handler)
app.add_exception_handler(Exception, exceptions.generic_exception_handler)
app.add_exception_handler(SQLAlchemyError, exceptions.sqlalchemy_exception_handler)

@app.get("/")
def healthcheck():
    return {"status": "ok"}