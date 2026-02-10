import pytest
from decimal import Decimal
from datetime import datetime

from app.domain.entities.address import Address
from app.domain.enums.address_enum import CountryEnum, StateEnum
from app.domain.value_objects.address.zipcode import ZipCode
from app.domain.value_objects.address.latitude import Latitude
from app.domain.value_objects.address.longitude import Longitude
from app.domain.exceptions.address_exceptions import InvalidAddressCoordinates, InvalidAddressField, InvalidCountry, InvalidState, InvalidZipCode
from app.domain.exceptions.domain_exception import AlreadyDeleted, CannotBeRestored, FieldTooLong
from app.domain.constants.address_constants import (
    ADDRESS_CITY_MAX_LENGTH,
    ADDRESS_NEIGHBORHOOD_MAX_LENGTH,
    ADDRESS_STREET_MAX_LENGTH,
    ADDRESS_NUMBER_MAX_LENGTH,
    ADDRESS_COMPLEMENT_MAX_LENGTH
)

@pytest.fixture
def valid_address_data():
    return {
        "id": 1,
        "zip_code": "90020-000",
        "country": "BR",
        "state": "RS",
        "city": "Porto Alegre",
        "neighborhood": "Centro Histórico",
        "street": "Rua dos Andradas",
        "number": "420",
        "complement": "1101",
        "latitude": Decimal("-29.263545"),
        "longitude": Decimal("-51.736234"),
        "deleted_at": None
    }

# -------------------- TEST ADDRESS CREATION --------------------

def test_address_creation(valid_address_data):
    address = Address(**valid_address_data)
    assert address.zip_code == ZipCode("90020000")
    assert address.country == CountryEnum.BR
    assert address.state == StateEnum.RS
    assert address.city == "Porto Alegre"
    assert address.neighborhood == "Centro Histórico"
    assert address.street == "Rua dos Andradas"
    assert address.number == "420"
    assert address.complement == "1101"
    assert address.latitude == Latitude(Decimal("-29.263545"))
    assert address.longitude == Longitude(Decimal("-51.736234"))
    assert address.deleted_at == None

def test_address_creation_none_coordinates(valid_address_data):
    valid_address_data["latitude"] = None
    valid_address_data["longitude"] = None
    address = Address(**valid_address_data)
    assert address.zip_code == ZipCode("90020000")
    assert address.country == CountryEnum.BR
    assert address.state == StateEnum.RS
    assert address.city == "Porto Alegre"
    assert address.neighborhood == "Centro Histórico"
    assert address.street == "Rua dos Andradas"
    assert address.number == "420"
    assert address.complement == "1101"
    assert address.latitude == None
    assert address.longitude == None
    assert address.deleted_at == None

def test_address_creation_invalid_coordinates(valid_address_data):
    valid_address_data["latitude"] = None
    with pytest.raises(InvalidAddressCoordinates):
        Address(**valid_address_data)


# -------------------- TEST FIELDS --------------------

@pytest.mark.parametrize(
    "field_name",
    ["neighborhood", "complement"]
)
def test_optional_fields_can_be_none(valid_address_data, field_name):
    valid_address_data[field_name] = None
    address = Address(**valid_address_data)
    assert getattr(address, field_name) is None

@pytest.mark.parametrize(
    "field_name",
    ["city", "street", "number"]
)
def test_fields_cannot_be_empty(valid_address_data, field_name):
    valid_address_data[field_name] = ""
    with pytest.raises(InvalidAddressField):
        Address(**valid_address_data)

def test_address_requires_zipcode(valid_address_data):
    valid_address_data["zip_code"] = None
    with pytest.raises(InvalidZipCode):
        Address(**valid_address_data)

def test_address_requires_country(valid_address_data):
    valid_address_data["country"] = None
    with pytest.raises(InvalidCountry):
        Address(**valid_address_data)    

def test_address_requires_state(valid_address_data):
    valid_address_data["state"] = None
    with pytest.raises(InvalidState):
        Address(**valid_address_data)     


@pytest.mark.parametrize(
    "field_name,max_length",
    [
        ("city", ADDRESS_CITY_MAX_LENGTH),
        ("street", ADDRESS_STREET_MAX_LENGTH),
        ("number", ADDRESS_NUMBER_MAX_LENGTH),
        ("neighborhood", ADDRESS_NEIGHBORHOOD_MAX_LENGTH),
        ("complement", ADDRESS_COMPLEMENT_MAX_LENGTH)
    ]
)
def test_fields_too_long(valid_address_data, field_name, max_length):
    valid_address_data[field_name] = "A" * (max_length + 1)
    with pytest.raises(FieldTooLong):
        Address(**valid_address_data)


# -------------------- TEST DELETED_AT --------------------

def test_is_deleted_reflects_deleted_at(valid_address_data):
    address = Address(**valid_address_data)
    assert address.is_deleted is False
    address.soft_delete()
    assert address.is_deleted is True


# -------------------- TEST SOFT_DELETE --------------------

def test_soft_delete_sets_deleted_at(valid_address_data):
    address = Address(**valid_address_data)
    address.soft_delete()
    assert address.deleted_at is not None


def test_soft_deleted_twice_raises_exception(valid_address_data):
    address = Address(**valid_address_data)
    address.soft_delete()
    with pytest.raises(AlreadyDeleted):
        address.soft_delete()


# -------------------- TEST RESTORE --------------------

def test_restore_clears_deleted_at(valid_address_data):
    address = Address(**valid_address_data)
    address.soft_delete()
    address.restore()
    assert address.deleted_at is None


def test_restore_without_delete_raises_exception(valid_address_data):
    address = Address(**valid_address_data)
    with pytest.raises(CannotBeRestored):
        address.restore()


# -------------------- TEST UPDATE_BASIC_INFO --------------------

def test_update_basic_info_updates_complement(valid_address_data):
    address = Address(**valid_address_data)
    address.update_basic_info(complement="Apto 202")
    assert address.complement == "Apto 202"


def test_update_basic_info_with_none_does_nothing(valid_address_data):
    address = Address(**valid_address_data)
    original = address.complement
    address.update_basic_info(complement=None)
    assert address.complement == original


def test_update_basic_info_complement_too_long(valid_address_data):
    address = Address(**valid_address_data)
    long_value = "x" * (ADDRESS_COMPLEMENT_MAX_LENGTH + 1)
    with pytest.raises(FieldTooLong):
        address.update_basic_info(complement=long_value)


# -------------------- TEST UPDATE_GEOCODING --------------------

def test_update_geocoding_updates_coordinates(valid_address_data):
    address = Address(**valid_address_data)
    lat = Latitude.from_raw("-29.0")
    lng = Longitude.from_raw("-51.0")
    address.update_geocoding(latitude=lat, longitude=lng)
    assert address.latitude == lat
    assert address.longitude == lng


def test_update_geocoding_can_clear_coordinates(valid_address_data):
    address = Address(**valid_address_data)
    address.update_geocoding(latitude=None, longitude=None)
    assert address.latitude is None
    assert address.longitude is None


def test_update_geocoding_partial_coordinates_is_invalid(valid_address_data):
    address = Address(**valid_address_data)
    lat = Latitude.from_raw("-29.0")
    with pytest.raises(InvalidAddressCoordinates):
        address.update_geocoding(latitude=lat, longitude=None)


# -------------------- TEST  --------------------

