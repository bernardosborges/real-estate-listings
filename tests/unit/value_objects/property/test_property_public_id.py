import pytest

from app.domain.value_objects.property.property_public_id import PropertyPublicId, PROPERTY_PUBLIC_ID_SIZE
from app.domain.exceptions.property_exceptions import InvalidPropertyPublicId


def test_property_public_id_valid():
    value = "abc123abc123abc123abc"
    public_id = PropertyPublicId.from_raw(value)
    assert isinstance(public_id, PropertyPublicId)
    assert public_id == value

def test_property_public_id_normalizes_value():
    value = "ABC123ABC123ABC123ABC"
    public_id = PropertyPublicId.from_raw(value)
    assert public_id == "abc123abc123abc123abc"

def test_property_public_id_exact_size():
    value = "a" * PROPERTY_PUBLIC_ID_SIZE
    public_id = PropertyPublicId.from_raw(value)
    assert public_id == value

def test_property_public_id_too_short():
    value = "a" * (PROPERTY_PUBLIC_ID_SIZE - 1)
    with pytest.raises(InvalidPropertyPublicId):
        PropertyPublicId.from_raw(value)

def test_property_public_id_too_long():
    value = "a" * (PROPERTY_PUBLIC_ID_SIZE + 1)
    with pytest.raises(InvalidPropertyPublicId):
        PropertyPublicId.from_raw(value)

def test_property_public_id_invalid_character():
    value = "abc123abc123abc123ab!"
    with pytest.raises(InvalidPropertyPublicId):
        PropertyPublicId.from_raw(value)

def test_property_public_id_uppercase_is_allowed_via_normalization():
    value = "ABC123ABC123ABC123ABC"
    public_id = PropertyPublicId.from_raw(value)
    assert public_id == value.lower()

def test_property_public_id_spaces_inside_are_invalid():
    value = "abc123abc123 abc123ab"
    with pytest.raises(InvalidPropertyPublicId):
        PropertyPublicId.from_raw(value)

def test_property_public_id_is_empty_string():
    with pytest.raises(InvalidPropertyPublicId):
        PropertyPublicId.from_raw("")

def test_property_public_id_only_number_is_valid():
    value = "1" * PROPERTY_PUBLIC_ID_SIZE
    public_id = PropertyPublicId.from_raw(value)
    assert public_id == value

def test_property_public_id_type():
    value = "a" * PROPERTY_PUBLIC_ID_SIZE
    public_id = PropertyPublicId.from_raw(value)
    assert type(public_id) is PropertyPublicId
    assert isinstance(public_id, str)

def test_property_public_id_non_string_value():
    with pytest.raises(InvalidPropertyPublicId):
        PropertyPublicId.from_raw(123)