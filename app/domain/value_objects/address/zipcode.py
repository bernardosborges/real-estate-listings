from __future__ import annotations
import re

from app.domain.exceptions.address_exceptions import InvalidZipCode
from app.domain.constants.address_constants import ADDRESS_ZIPCODE_LENGTH

class ZipCode:

    __slots__ = ("_value",)

    _REGEX = re.compile(rf"^\d{{{ADDRESS_ZIPCODE_LENGTH}}}$")

    def __init__(self, normalized: str):
        self._value = normalized

    @classmethod
    def from_raw(cls, value: str) -> ZipCode:
        if not isinstance(value, str):
            raise InvalidZipCode("ZipCode must be a string")

        normalized = re.sub(r"\D", "", value) #cls._normalize(value)
        if not cls._REGEX.fullmatch(normalized):
            raise InvalidZipCode(f"ZipCode must have exaclty {ADDRESS_ZIPCODE_LENGTH} numeric digits. Value: '{value}'")
        #cls._validate(normalized)

        return cls(normalized)


    @property
    def value(self) -> str:
        return self._value

    @property
    def formatted(self) -> str:
        return f"{self.value[:5]}-{self.value[5:]}"

    def __eq__(self, other):
        return isinstance(other, ZipCode) and self.value == other.value

    def __repr__(self):
        return f"ZipCode('{self.formatted}')"

    def __str__(self) -> str:
        return self.value


    @staticmethod
    def _normalize(value: str) -> str:
        return re.sub(r"\D", "", value)

    @staticmethod
    def _validate(cls, value: str) -> None:
        if not cls._REGEX.fullmatch(value):
            raise InvalidZipCode("ZipCode must have exaclty {ADDRESS_ZIPCODE_LENGTH} numeric digits. Value: '{value}'")
