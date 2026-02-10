from decimal import Decimal


class UpdateAddressInput:

    def __init__(
            self,
            number: str | None = None,
            complement: str | None = None,
            latitude: Decimal | None = None,
            longitude: Decimal | None = None,
            confidence: float | None = None,
            provider: str | None = None
    ):
        self.number = number
        self.complement = complement
        self.latitude = latitude
        self.longitude = longitude
        self.confidence = confidence
        self.provider = provider
