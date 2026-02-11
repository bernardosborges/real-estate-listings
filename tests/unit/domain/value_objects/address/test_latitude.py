import pytest
from decimal import Decimal

from app.domain.value_objects.address.latitude import Latitude
from app.domain.exceptions.address_exceptions import InvalidLatitude


def test_latitude_creation_from_string():
    lat = Latitude.from_raw("10.12345")
    assert lat == Latitude.from_raw(Decimal("10.12345"))


def test_latitude_is_quantized_to_6_decimal_places():
    lat = Latitude.from_raw("10.123456789")
    assert lat.value == Decimal("10.123457")


@pytest.mark.parametrize(
    "value",
    ["-90","90", Decimal("-90.0"), Decimal("90.0")]
)
def test_latitude_accepts_boundary_values(value):
    lat = Latitude.from_raw(value)
    assert lat.value == Decimal(value).quantize(Decimal("0.000001"))


@pytest.mark.parametrize(
    "value",
    ["-90.000001","90.000001", "-100", "100"]
)
def test_latitude_out_of_range_raises_exception(value):
    with pytest.raises(InvalidLatitude):
        lat = Latitude.from_raw(value)


@pytest.mark.parametrize(
    "value",
    [None, "abc", {}, [], object()]
)
def test_latitude_invalid_type_raises_exception(value):
    with pytest.raises(InvalidLatitude):
        lat = Latitude.from_raw(value)
    

def test_latitude_equality():
    lat1 = Latitude.from_raw("10.1234564")
    lat2 = Latitude.from_raw(Decimal("10.123456"))
    assert lat1 == lat2

def test_latitude_repr():
    lat = Latitude.from_raw("10.5")
    assert repr(lat) == "Latitude(10.500000)"