import pytest

from app.domain.value_objects.address.zipcode import ZipCode
from app.domain.exceptions.address_exceptions import InvalidZipCode


@pytest.mark.unit
def test_zipcode_creation_with_plan_digits():
    zip_code = ZipCode.from_raw("12345678")
    assert zip_code.value == "12345678"


@pytest.mark.unit
def test_zipcode_normalizes_formatted_value():
    zip_code = ZipCode.from_raw("12345-678")
    assert zip_code.value == "12345678"


@pytest.mark.unit
@pytest.mark.parametrize("value", ["12.345-678", "12 345 678", "(12)345-678"])
def test_zipcode_normalizes_various_formats(value):
    zip_code = ZipCode.from_raw(value)
    assert zip_code.value == "12345678"


@pytest.mark.unit
@pytest.mark.parametrize("value", [None, 12345678, 12.34, [], {}])
def test_zipcode_non_string_raises_exception(value):
    with pytest.raises(InvalidZipCode):
        ZipCode.from_raw(value)


@pytest.mark.unit
@pytest.mark.parametrize("value", ["1234", "1234567", "12.345-67"])
def test_zipcode_too_short_raises_exception(value):
    with pytest.raises(InvalidZipCode):
        ZipCode.from_raw(value)


@pytest.mark.unit
@pytest.mark.parametrize("value", ["123456789", "12345-6789"])
def test_zipcode_too_long_raises_exception(value):
    with pytest.raises(InvalidZipCode):
        ZipCode.from_raw(value)


@pytest.mark.unit
@pytest.mark.parametrize("value", ["abcdefgh", "1234abcd", "!!!!----"])
def test_zipcode_invalid_characters_raises_exception(value):
    with pytest.raises(InvalidZipCode):
        ZipCode.from_raw(value)


@pytest.mark.unit
def test_zipcode_equality_after_normalization():
    zip1 = ZipCode.from_raw("12345-678")
    zip2 = ZipCode.from_raw("12345678")
    assert zip1 == zip2


@pytest.mark.unit
def test_zipcode_formatted_property():
    zip_code = ZipCode.from_raw("12345678")
    assert zip_code.formatted == "12345-678"


@pytest.mark.unit
def test_zipcode_str_returns_raw_value():
    zip_code = ZipCode.from_raw("12345-678")
    assert str(zip_code) == "12345678"


@pytest.mark.unit
def test_zipcode_repr():
    zip_code = ZipCode.from_raw("12345678")
    assert repr(zip_code) == "ZipCode('12345-678')"
