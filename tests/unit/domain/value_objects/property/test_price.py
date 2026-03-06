import pytest
from decimal import Decimal

from app.domain.value_objects.property.price import Price
from app.domain.exceptions.property_exceptions import InvalidPrice


@pytest.mark.unit
def test_price_from_decimal():
    price = Price.from_raw(Decimal("10.50"))
    assert price.value == Decimal("10.50")


@pytest.mark.unit
def test_price_from_string():
    price = Price.from_raw("99.99")
    assert price.value == Decimal("99.99")


@pytest.mark.unit
def test_price_from_float():
    price = Price.from_raw(10.1)
    assert price.value == Decimal("10.10")


@pytest.mark.unit
def test_price_rounding_half_up():
    price = Price.from_raw("10.005")
    assert price.value == Decimal("10.01")


@pytest.mark.unit
def test_price_zero_is_valid():
    price = Price.from_raw("0")
    assert price.value == Decimal("0.00")


@pytest.mark.unit
def test_price_max_value():
    price = Price.from_raw(Price.MAX_VALUE)
    assert price.value == Price.MAX_VALUE


@pytest.mark.unit
def test_price_negative_raises_exception():
    with pytest.raises(InvalidPrice, match="Price cannot be negative"):
        Price.from_raw("-1.00")


@pytest.mark.unit
def test_price_exceeds_max_value():
    value = Price.MAX_VALUE + Decimal("0.01")
    with pytest.raises(InvalidPrice, match="Price exceeds maximum allowed"):
        Price.from_raw(value)


@pytest.mark.unit
def test_price_invalid_value_raises_exception():
    with pytest.raises(InvalidPrice, match="Cannot convert"):
        Price.from_raw("abc")


@pytest.mark.unit
def test_price_equality():
    price1 = Price.from_raw("10.00")
    price2 = Price.from_raw(Decimal("10.0"))
    price3 = Price.from_raw("10.01")
    assert price1 == price2
    assert price1 != price3


@pytest.mark.unit
def test_price_repr():
    price = Price.from_raw("12.34")
    assert repr(price) == "Price(12.34)"
