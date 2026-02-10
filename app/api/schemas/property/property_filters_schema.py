from pydantic import BaseModel, field_validator
from decimal import Decimal
from fastapi import Query

from app.api.exceptions.schema_exceptions import InvalidPriceFilters

class PropertyFiltersSchema(BaseModel):

    price_min: Decimal | None = Query(None, ge=0, description="Minimum price")
    price_max: Decimal | None = Query(None, ge=0, description="Maximum price")
    limit: int = Query(10, ge=1, le=100, description="Maximum number of results")
    offset: int = Query(0, ge=0, description="Number of results do skip")

    @field_validator("price_max")
    def validate_price_range(cls, v, info):
        
        max_price = v
        if max_price is not None:
            min_price = info.data.get("price_min")
            if min_price is not None and max_price < min_price:
                raise InvalidPriceFilters()
        return max_price
        