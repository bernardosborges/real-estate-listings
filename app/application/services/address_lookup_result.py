from dataclasses import dataclass


@dataclass(frozen=True)
class AddressLookupResult:
    zip_code: str
    country: str
    state: str
    city: str
    neighborhood: str
    street: str