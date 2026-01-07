from fastapi import FastAPI
from app.routers import property_router

app = FastAPI(
    title="Real Estate Listing API",
    version="0.1.0"
)


API_PREFIX = "/api/v0"
app.include_router(property_router.router, prefix=API_PREFIX)

@app.get("/")
def healthcheck():
    return {"status": "ok"}