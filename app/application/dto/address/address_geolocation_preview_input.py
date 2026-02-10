from dataclasses import dataclass


@dataclass(frozen=True)
class AddressGeolocationPreviewInput:
    zip_code: str
    country: str
    state: str
    city: str
    neighborhood: str | None
    street: str
    number: str