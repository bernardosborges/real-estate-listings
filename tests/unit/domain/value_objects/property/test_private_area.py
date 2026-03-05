import pytest
from decimal import Decimal

from app.domain.value_objects.property.private_area import PrivateArea
from app.domain.exceptions.property_exceptions import InvalidPrivateArea


@pytest.mark.unit
def test_private_area_from_decimal():
    private_area = PrivateArea.from_raw(Decimal("120.50"))
    assert private_area.value == Decimal("120.50")


@pytest.mark.unit
def test_private_area_from_string():
    private_area = PrivateArea.from_raw("85.75")
    assert private_area.value == Decimal("85.75")


@pytest.mark.unit
def test_private_area_from_float():
    private_area = PrivateArea.from_raw(10.1)
    assert private_area.value == Decimal("10.10")


@pytest.mark.unit
def test_private_area_rounding_half_up():
    private_area = PrivateArea.from_raw("10.005")
    assert private_area.value == Decimal("10.01")


@pytest.mark.unit
def test_private_area_zero_is_valid():
    private_area = PrivateArea.from_raw("0")
    assert private_area.value == Decimal("0.00")


@pytest.mark.unit
def test_private_area_max_value():
    private_area = PrivateArea.from_raw(PrivateArea.MAX_VALUE)
    assert private_area.value == PrivateArea.MAX_VALUE


@pytest.mark.unit
def test_private_area_negative_raises_exception():
    with pytest.raises(InvalidPrivateArea, match="Private area cannot be negative"):
        PrivateArea.from_raw("-1.00")


@pytest.mark.unit
def test_private_area_exceeds_max_value():
    value = PrivateArea.MAX_VALUE + Decimal("0.01")
    with pytest.raises(InvalidPrivateArea, match="Private area exceeds maximum allowed"):
        PrivateArea.from_raw(value)


@pytest.mark.unit
def test_private_area_invalid_value_raises_exception():
    with pytest.raises(InvalidPrivateArea, match="Cannot convert"):
        PrivateArea.from_raw("abc")


@pytest.mark.unit
def test_private_area_equality():
    private_area1 = PrivateArea.from_raw("100.00")
    private_area2 = PrivateArea.from_raw(Decimal("100.0"))
    private_area3 = PrivateArea.from_raw("100.01")
    assert private_area1 == private_area2
    assert private_area1 != private_area3


@pytest.mark.unit
def test_private_area_repr():
    private_area = PrivateArea.from_raw("75.25")
    assert repr(private_area) == "PrivateArea(75.25)"
