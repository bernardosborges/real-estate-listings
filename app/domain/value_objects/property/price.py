from __future__ import annotations
from decimal import Decimal, ROUND_HALF_UP

from app.domain.exceptions.property_exceptions import InvalidPrice

class Price:
    __slots__ = ("_value",)

    MAX_VALUE = Decimal("999999999999.99") # 12 + 2 digits (999.999.999.999.99)

    def __init__(self, value: Decimal):
        self._value = value

    @classmethod
    def from_raw(cls, value: str | float | Decimal) -> Price:
        if not isinstance(value, Decimal):
            try:
                value = Decimal(value)
            except Exception:
                raise InvalidPrice(f"Cannot convert {value} to Decimal")
        
        value = value.quantize(
            Decimal("0.01"),
            rounding = ROUND_HALF_UP
        )

        if value < 0:
            raise InvalidPrice("Price cannot be negative")
        
        if value > cls.MAX_VALUE:
            raise InvalidPrice("Price exceeds maximum allowed")
        
        return cls(value)

    @property
    def value(self) -> Decimal:
        return self._value


    def __eq__(self, other):
        return isinstance(other, Price) and self.value == other.value
    
    def __repr__(self):
        return f"Price({self.value})"