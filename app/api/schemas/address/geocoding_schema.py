import re
from decimal import Decimal

from pydantic import BaseModel, Field, field_validator

# -----------------------------------------------
# BASE
# -----------------------------------------------

class GeolocationPreviewRequestSchema(BaseModel):
    zip_code: str = Field(..., min_length=8, max_length=8)
    country: str = Field(..., min_length=2, max_length=2)
    state: str = Field(..., min_length=2, max_length=2)
    city: str
    neighborhood: str | None = None
    street: str
    number: str

    model_config = {
        "title": "GeolocationPreviewRequestSchema",
        "from_attributes": True,
    }

    @field_validator("zip_code", mode="before")
    def normalize_and_validate_zip_code(cls, v):
        if v is None:
            raise ValueError("Zip code is required.")
        digits = re.sub(r"\D", "", v)
        if len(digits) != 8:
            raise ValueError("Invalid zip code. It must contain exactly 8 digits.")
        return digits
    

    @field_validator("country", "state", mode="before")
    def normalize_country_and_state(cls, v: str) -> str:
        if not v:
            raise ValueError("Value is required.")
        
        value = v.strip().upper()

        if len(value) != 2:
            raise ValueError("Value must contain exactly 2 characters.")
        
        return value
    
    
    @field_validator("city", "neighborhood", "street", mode="before")
    def normalize_text(cls, v):
        if v is None:
            return v
        return " ".join(v.strip().split())
    

    @field_validator("number", mode="before")
    def normalize_number(cls, v):
        if not v:
            raise ValueError("Number is required.")
        return v.strip()
    

class GeolocationPreviewResponseSchema(BaseModel):
    latitude: Decimal
    longitude: Decimal
    confidence: float
    provider: str


    model_config = {
        "title": "GeolocationPreviewResponseSchema",
        "from_attributes": True,
    }