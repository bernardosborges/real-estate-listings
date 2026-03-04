from __future__ import annotations
import re
from app.domain.exceptions.property_exceptions import InvalidPropertyPublicId

ALPHABET = "abcdefghijklmnopqrstuvwxyz0123456789"
PROPERTY_PUBLIC_ID_SIZE = 21
PROPERTY_PUBLIC_ID_REGEX = re.compile(rf"^[{ALPHABET}]{{{PROPERTY_PUBLIC_ID_SIZE}}}$")


class PropertyPublicId(str):

    @classmethod
    def from_raw(cls, value: str) -> "PropertyPublicId":
        normalized = cls._normalize(value)
        cls._validate(normalized)

        return cls(normalized)

    @staticmethod
    def _normalize(value: str) -> str:
        if not isinstance(value, str):
            raise InvalidPropertyPublicId(value)
        return value.strip().lower()

    @staticmethod
    def _validate(value: str) -> None:
        if not PROPERTY_PUBLIC_ID_REGEX.fullmatch(value):
            raise InvalidPropertyPublicId(value)
