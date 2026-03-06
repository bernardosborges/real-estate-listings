import pytest
from decimal import Decimal

from app.application.usecases.property.create_property import CreatePropertyUseCase
from app.application.dto.property.create_property_input import CreatePropertyInput
from app.application.dto.address.address_input import AddressInput
from app.domain.exceptions.user_profile_exceptions import UserProfileNotFound


def make_valid_input():
    return CreatePropertyInput(
        description="Test home",
        price=Decimal("100000.00"),
        private_area=Decimal("120.00"),
        address=AddressInput(
            zip_code="12345678",
            country="BR",
            state="RS",
            city="Porto Alegre",
            neighborhood="Centro",
            street="Rua A",
            number="100",
            complement=None,
            latitude=None,
            longitude=None,
        ),
    )


@pytest.mark.unit
def test_should_raise_when_profile_not_found(fake_uow, user_factory_fixture):
    user = user_factory_fixture()
    input_dto = make_valid_input()

    usecase = CreatePropertyUseCase(fake_uow)

    with pytest.raises(UserProfileNotFound):
        usecase.execute(input_dto, user)

    assert fake_uow.committed is False


@pytest.mark.unit
def test_should_create_new_address_when_not_exists(fake_uow, user_factory_fixture, user_profile_factory_fixture):
    user = user_factory_fixture()
    user_profile = user_profile_factory_fixture(user_id=user.id)
    fake_uow.profile_repository.save(user_profile)
    input_dto = make_valid_input()

    usecase = CreatePropertyUseCase(fake_uow)

    output = usecase.execute(input_dto, user)

    assert fake_uow.committed is True
    assert len(fake_uow.address_repository._addresses) == 1
    assert len(fake_uow.property_repository._properties) == 1
    assert output.description == "Test home"


@pytest.mark.unit
def test_should_reuse_existing_address(
    fake_uow, user_factory_fixture, user_profile_factory_fixture, address_factory_fixture
):
    user = user_factory_fixture()
    user_profile = user_profile_factory_fixture(user_id=user.id)
    fake_uow.profile_repository.save(user_profile)

    existing_address = address_factory_fixture(
        zip_code="12345678",
        country="BR",
        state="RS",
        city="Porto Alegre",
        neighborhood="Centro",
        street="Rua A",
        number="100",
        complement=None,
    )

    fake_uow.address_repository.save(existing_address)
    input_dto = make_valid_input()

    usecase = CreatePropertyUseCase(fake_uow)

    usecase.execute(input_dto, user)

    assert len(fake_uow.address_repository._addresses) == 1
    assert len(fake_uow.property_repository._properties) == 1
    assert fake_uow.committed is True


@pytest.mark.unit
def test_should_associate_property_with_profile(fake_uow, user_factory_fixture, user_profile_factory_fixture):
    user = user_factory_fixture()
    profile = user_profile_factory_fixture(user_id=user.id)
    fake_uow.profile_repository.save(profile)

    input_dto = make_valid_input()
    usecase = CreatePropertyUseCase(fake_uow)

    usecase.execute(input_dto, user)

    property_saved = fake_uow.property_repository._properties[0]
    assert property_saved.profile_id == profile.id
