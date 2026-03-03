from __future__ import annotations
from decimal import Decimal, ROUND_HALF_UP, InvalidOperation

from app.domain.exceptions.address_exceptions import InvalidLongitude


class Longitude:
    __slots__ = ("_value",)

    MIN = Decimal("-180.0")
    MAX = Decimal("180.0")

    def __init__(self, value: Decimal):
        self._value = value

    @classmethod
    def from_raw(cls, value: str | int | float | Decimal) -> Longitude:

        try:
            decimal_value = Decimal(str(value))
        except (InvalidOperation, ValueError, TypeError):
            raise InvalidLongitude(f"Invalid longitude value: '{value}'.")

        decimal_value = decimal_value.quantize(
            Decimal("0.000001"),
            rounding = ROUND_HALF_UP
        )

        if decimal_value < cls.MIN or decimal_value > cls.MAX:
            raise InvalidLongitude("Longitude must be between -180 and 180. Value: '{value}'")

        return cls(decimal_value)

    @property
    def value(self) -> Decimal:
        return self._value


    def __eq__(self, other):
        return isinstance(other, Longitude) and self.value == other.value

    def __repr__(self):
        return f"Longitude({self.value})"
