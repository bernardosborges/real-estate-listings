import pytest
from decimal import Decimal

from app.domain.enums.address_enum import CountryEnum, StateEnum
from app.domain.value_objects.address.zipcode import ZipCode
from app.domain.value_objects.address.latitude import Latitude
from app.domain.value_objects.address.longitude import Longitude
from app.domain.exceptions.address_exceptions import (
    InvalidAddressCoordinates,
    InvalidAddressField,
    InvalidCountry,
    InvalidState,
    InvalidZipCode,
)
from app.domain.exceptions.domain_exception import AlreadyDeleted, CannotBeRestored, FieldTooLong
from app.domain.constants.address_constants import (
    ADDRESS_CITY_MAX_LENGTH,
    ADDRESS_NEIGHBORHOOD_MAX_LENGTH,
    ADDRESS_STREET_MAX_LENGTH,
    ADDRESS_NUMBER_MAX_LENGTH,
    ADDRESS_COMPLEMENT_MAX_LENGTH,
)

# -------------------- TEST ADDRESS CREATION --------------------


@pytest.mark.unit
def test_address_creation(address_factory_fixture):
    address = address_factory_fixture()
    assert address.zip_code == ZipCode("90020000").formatted
    assert address.country == CountryEnum.BR.value
    assert address.state == StateEnum.RS.value
    assert address.city == "Porto Alegre"
    assert address.neighborhood == "Centro Histórico"
    assert address.street == "Rua dos Andradas"
    assert address.number == "420"
    assert address.complement == "1101"
    assert address.latitude == Latitude(Decimal("-29.263545")).value
    assert address.longitude == Longitude(Decimal("-51.736234")).value
    assert address.deleted_at is None


@pytest.mark.unit
def test_address_creation_none_coordinates(address_factory_fixture):
    address = address_factory_fixture(latitude=None, longitude=None)
    assert address.latitude is None
    assert address.longitude is None


@pytest.mark.unit
def test_address_creation_invalid_coordinates(address_factory_fixture):
    with pytest.raises(InvalidAddressCoordinates):
        address_factory_fixture(latitude=None)


# -------------------- TEST FIELDS --------------------


@pytest.mark.unit
@pytest.mark.parametrize("field_name", ["neighborhood", "complement"])
def test_optional_fields_can_be_none(address_factory_fixture, field_name):
    address = address_factory_fixture(**{field_name: None})
    assert getattr(address, field_name) is None


@pytest.mark.unit
@pytest.mark.parametrize(
    "field_name,max_length",
    [
        ("city", ADDRESS_CITY_MAX_LENGTH),
        ("street", ADDRESS_STREET_MAX_LENGTH),
        ("number", ADDRESS_NUMBER_MAX_LENGTH),
        ("neighborhood", ADDRESS_NEIGHBORHOOD_MAX_LENGTH),
        ("complement", ADDRESS_COMPLEMENT_MAX_LENGTH),
    ],
)
def test_fields_too_long(address_factory_fixture, field_name, max_length):
    with pytest.raises(FieldTooLong):
        address_factory_fixture(**{field_name: "A" * (max_length + 1)})


@pytest.mark.unit
@pytest.mark.parametrize("field_name", ["city", "street", "number"])
def test_fields_cannot_be_empty(address_factory_fixture, field_name):
    with pytest.raises(InvalidAddressField):
        address_factory_fixture(**{field_name: ""})


@pytest.mark.unit
def test_address_requires_zipcode(address_factory_fixture):
    with pytest.raises(InvalidZipCode):
        address_factory_fixture(zip_code=None)


@pytest.mark.unit
def test_address_requires_country(address_factory_fixture):
    with pytest.raises(InvalidCountry):
        address_factory_fixture(country=None)


@pytest.mark.unit
def test_address_requires_state(address_factory_fixture):
    with pytest.raises(InvalidState):
        address_factory_fixture(state=None)


# -------------------- TEST IS_DELETED  --------------------


@pytest.mark.unit
def test_is_deleted_reflects_deleted_at(address_factory_fixture):
    address = address_factory_fixture()
    assert address.is_deleted is False
    address.soft_delete()
    assert address.is_deleted is True


# -------------------- TEST SOFT_DELETE --------------------


@pytest.mark.unit
def test_soft_delete_sets_deleted_at(address_factory_fixture):
    address = address_factory_fixture()
    address.soft_delete()
    assert address.deleted_at is not None


@pytest.mark.unit
def test_soft_deleted_twice_raises_exception(address_factory_fixture):
    address = address_factory_fixture()
    address.soft_delete()
    with pytest.raises(AlreadyDeleted):
        address.soft_delete()


# -------------------- TEST RESTORE --------------------


@pytest.mark.unit
def test_restore_clears_deleted_at(address_factory_fixture):
    address = address_factory_fixture()
    address.soft_delete()
    address.restore()
    assert address.deleted_at is None


@pytest.mark.unit
def test_restore_without_delete_raises_exception(address_factory_fixture):
    address = address_factory_fixture()
    with pytest.raises(CannotBeRestored):
        address.restore()


# -------------------- TEST UPDATE_BASIC_INFO --------------------


@pytest.mark.unit
def test_update_basic_info_updates_complement(address_factory_fixture):
    address = address_factory_fixture()
    address.update_basic_info(complement="Apto 202")
    assert address.complement == "Apto 202"


@pytest.mark.unit
def test_update_basic_info_with_none_does_nothing(address_factory_fixture):
    address = address_factory_fixture()
    original = address.complement
    address.update_basic_info(complement=None)
    assert address.complement == original


@pytest.mark.unit
def test_update_basic_info_complement_too_long(address_factory_fixture):
    address = address_factory_fixture()
    long_value = "x" * (ADDRESS_COMPLEMENT_MAX_LENGTH + 1)
    with pytest.raises(FieldTooLong):
        address.update_basic_info(complement=long_value)


# -------------------- TEST UPDATE_GEOCODING --------------------


@pytest.mark.unit
def test_update_geocoding_updates_coordinates(address_factory_fixture):
    address = address_factory_fixture()
    lat = Latitude.from_raw("-29.0")
    lng = Longitude.from_raw("-51.0")
    address.update_geocoding(latitude=lat, longitude=lng)
    assert address.latitude == lat
    assert address.longitude == lng


@pytest.mark.unit
def test_update_geocoding_can_clear_coordinates(address_factory_fixture):
    address = address_factory_fixture()
    address.update_geocoding(latitude=None, longitude=None)
    assert address.latitude is None
    assert address.longitude is None


@pytest.mark.unit
def test_update_geocoding_partial_coordinates_is_invalid(address_factory_fixture):
    address = address_factory_fixture()
    lat = Latitude.from_raw("-29.0")
    with pytest.raises(InvalidAddressCoordinates):
        address.update_geocoding(latitude=lat, longitude=None)
