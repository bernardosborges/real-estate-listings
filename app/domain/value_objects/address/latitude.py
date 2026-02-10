from __future__ import annotations
from decimal import Decimal, ROUND_HALF_UP, InvalidOperation

from app.domain.exceptions.address_exceptions import InvalidLatitude


class Latitude:
    __slots__ = ("_value",)


    MIN = Decimal("-90.0")
    MAX = Decimal("90.0")

    def __init__(self, value: Decimal):
        self._value = value

    @classmethod
    def from_raw(cls, value: str | int | float | Decimal) -> Latitude:
        
        try:
            decimal_value = Decimal(str(value))
        except (InvalidOperation, ValueError, TypeError):
            raise InvalidLatitude(f"Invalid latitude value: '{value}'.")

        decimal_value = decimal_value.quantize(
            Decimal("0.000001"),
            rounding = ROUND_HALF_UP
        )

        if decimal_value < cls.MIN or decimal_value > cls.MAX:
            raise InvalidLatitude("Latitude must be between -90 and 90. Value: '{value}'")

        return cls(decimal_value)


    @property
    def value(self) -> Decimal:
        return self._value


    def __eq__(self, other):
        return isinstance(other, Latitude) and self.value == other.value
    
    def __repr__(self):
        return f"Latitude({self.value})"