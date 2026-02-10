from __future__ import annotations
from decimal import Decimal, ROUND_HALF_UP

from app.domain.exceptions.property_exceptions import InvalidPrivateArea

class PrivateArea:
    __slots__ = ("_value",)

    MAX_VALUE = Decimal("9999999999.99") # 10 + 2 digits (9.999.999.999.99)

    def __init__(self, value: Decimal):
        self._value = value

    @classmethod
    def from_raw(cls, value: float | str | Decimal) -> PrivateArea:
        if not isinstance(value, Decimal):
            try:
                value = Decimal(value)
            except Exception:
                raise InvalidPrivateArea(f"Cannot convert {value} to Decimal")
        
        value = value.quantize(
            Decimal("0.01"),
            rounding = ROUND_HALF_UP
        )

        if value < 0:
            raise InvalidPrivateArea("Private area cannot be negative")
        
        if value > cls.MAX_VALUE:
            raise InvalidPrivateArea("Private area exceeds maximum allowed")
        
        return cls(value)

    @property
    def value(self) -> Decimal:
        return self._value


    def __eq__(self, other):
        return isinstance(other, PrivateArea) and self.value == other.value
    
    def __repr__(self):
        return f"PrivateArea({self.value})"