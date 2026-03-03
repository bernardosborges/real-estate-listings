from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class GeocodingResult:
    latitude: Decimal
    longitude: Decimal
    confidence: float | None
    provider: str
