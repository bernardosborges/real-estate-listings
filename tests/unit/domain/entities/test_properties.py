import pytest
from decimal import Decimal
from datetime import datetime, timezone

from app.domain.exceptions.domain_exception import (
    AlreadyActive,
    AlreadyDeactivated,
    CannotBeRestored,
    AlreadyDeleted,
    FieldTooLong,
)

from app.domain.constants.property_constants import (
    PROPERTY_DESCRIPTION_MAX_LENGHT,
)

from app.domain.value_objects.property.price import Price
from app.domain.value_objects.property.private_area import PrivateArea
from app.domain.value_objects.property.property_public_id import PropertyPublicId

# -----------------------------------------------
# TEST CREATION
# -----------------------------------------------


@pytest.mark.unit
def test_property_creation(property_factory_fixture):
    property = property_factory_fixture()
    assert property.id == 1
    assert property.public_id == PropertyPublicId("abc123abc123abc123abc")
    assert property.profile_id == "user7"
    assert property.description == "Apartamento padrão"
    assert property.price == Price(50000.00).value
    assert property.private_area == PrivateArea(80.00).value
    assert property.is_active
    assert property.deleted_at is None


# -----------------------------------------------
# TEST LIFECYCLE
# -----------------------------------------------

# -------------------- TEST IS_DELETED  --------------------


@pytest.mark.unit
def test_is_deleted_reflects_deleted_at_and_is_active(property_factory_fixture):
    property = property_factory_fixture(deleted_at=None)
    assert property.is_deleted is False
    property.soft_delete()
    assert property.is_deleted is True


# -------------------- TEST SOFT_DELETE --------------------


@pytest.mark.unit
def test_soft_delete_sets_deleted_at_and_is_active(property_factory_fixture):
    property = property_factory_fixture(deleted_at=None)
    property.soft_delete()
    assert property.deleted_at is not None
    assert property.is_active is False


@pytest.mark.unit
def test_soft_deleted_twice_raises_exception(property_factory_fixture):
    property = property_factory_fixture(deleted_at=datetime.now(timezone.utc))
    with pytest.raises(AlreadyDeleted):
        property.soft_delete()


# -------------------- TEST RESTORE --------------------


@pytest.mark.unit
def test_restore_clears_deleted_at_and_is_active(property_factory_fixture):
    property = property_factory_fixture(deleted_at=datetime.now(timezone.utc))
    property.restore()
    assert property.deleted_at is None
    assert property.is_active is True


@pytest.mark.unit
def test_restore_without_delete_raises_exception(property_factory_fixture):
    property = property_factory_fixture(deleted_at=None)
    with pytest.raises(CannotBeRestored):
        property.restore()


# -------------------- TEST ACTIVATE --------------------


@pytest.mark.unit
def test_activate_updates_is_active(property_factory_fixture):
    property = property_factory_fixture(is_active=False)
    property.activate()
    assert property.is_active


@pytest.mark.unit
def test_activate_twice_raises_exception(property_factory_fixture):
    property = property_factory_fixture(is_active=True)
    with pytest.raises(AlreadyActive):
        property.activate()


# -------------------- TEST DEACTIVATE --------------------


@pytest.mark.unit
def test_deactivate_updates_is_active(property_factory_fixture):
    property = property_factory_fixture(is_active=True)
    property.deactivate()
    assert not property.is_active


@pytest.mark.unit
def test_deactivate_twice_raises_exception(property_factory_fixture):
    property = property_factory_fixture(is_active=False)
    with pytest.raises(AlreadyDeactivated):
        property.deactivate()


# -----------------------------------------------
# TEST UPDATE
# -----------------------------------------------


@pytest.mark.unit
def test_update_description(property_factory_fixture):
    property = property_factory_fixture()
    property.update_basic_info(description="Nova descrição")
    assert property.description == "Nova descrição"


@pytest.mark.unit
def test_update_description_too_long(property_factory_fixture):
    property = property_factory_fixture()
    long_description = "A" * (PROPERTY_DESCRIPTION_MAX_LENGHT + 1)
    with pytest.raises(FieldTooLong):
        property.update_basic_info(description=long_description)


@pytest.mark.unit
def test_update_price(property_factory_fixture):
    property = property_factory_fixture()
    property.update_basic_info(price=Decimal(100000.00))
    assert property.price == Price(100000.00)


@pytest.mark.unit
def test_update_private_area(property_factory_fixture):
    property = property_factory_fixture()
    property.update_basic_info(private_area=Decimal(120.00))
    assert property.private_area == PrivateArea(120.00)


@pytest.mark.unit
def test_update_with_none_does_nothing(property_factory_fixture):
    property = property_factory_fixture()
    original_description = property.description
    original_price = property.price
    original_private_area = property.private_area
    property.update_basic_info(description=None, price=None, private_area=None)
    assert property.description == original_description
    assert property.price == original_price
    assert property.private_area == original_private_area
