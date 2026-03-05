import pytest
from decimal import Decimal

from app.domain.value_objects.address.longitude import Longitude
from app.domain.exceptions.address_exceptions import InvalidLongitude


def test_longitude_creation_from_string():
    lat = Longitude.from_raw("10.12345")
    assert lat == Longitude.from_raw(Decimal("10.12345"))


def test_longitude_is_quantized_to_6_decimal_places():
    lat = Longitude.from_raw("10.123456789")
    assert lat.value == Decimal("10.123457")


@pytest.mark.parametrize("value", ["-180", "180", Decimal("-180.0"), Decimal("180.0")])
def test_longitude_accepts_boundary_values(value):
    lat = Longitude.from_raw(value)
    assert lat.value == Decimal(value).quantize(Decimal("0.000001"))


@pytest.mark.parametrize("value", ["-180.000001", "180.000001", "-200", "200"])
def test_longitude_out_of_range_raises_exception(value):
    with pytest.raises(InvalidLongitude):
        Longitude.from_raw(value)


@pytest.mark.parametrize("value", [None, "abc", {}, [], object()])
def test_longitude_invalid_type_raises_exception(value):
    with pytest.raises(InvalidLongitude):
        Longitude.from_raw(value)


def test_longitude_equality():
    lat1 = Longitude.from_raw("10.1234564")
    lat2 = Longitude.from_raw(Decimal("10.123456"))
    assert lat1 == lat2


def test_longitude_repr():
    lat = Longitude.from_raw("10.5")
    assert repr(lat) == "Longitude(10.500000)"
