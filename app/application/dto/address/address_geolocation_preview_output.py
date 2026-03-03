from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class AddressGeolocationPreviewOutput:
    latitude: Decimal
    longitude: Decimal
    confidence: float
    provider: str
