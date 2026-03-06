import pytest

from app.domain.enums.address_enum import CountryEnum, StateEnum
from app.domain.exceptions.address_exceptions import InvalidCountry, InvalidState

# -------------------- TEST COUNTRY_ENUM --------------------


@pytest.mark.unit
def test_countryenum_valid():
    assert CountryEnum.from_raw("BR") == CountryEnum.BR
    assert CountryEnum.from_raw("br") == CountryEnum.BR
    assert CountryEnum.from_raw(" br ") == CountryEnum.BR


@pytest.mark.unit
def test_countryenum_invalid_value():
    with pytest.raises(InvalidCountry):
        CountryEnum.from_raw("BRR")
    with pytest.raises(InvalidCountry):
        CountryEnum.from_raw("US")
    with pytest.raises(InvalidCountry):
        CountryEnum.from_raw(" ")


@pytest.mark.unit
def test_countryenum_invalid_type():
    with pytest.raises(InvalidCountry):
        CountryEnum.from_raw(123)
    with pytest.raises(InvalidCountry):
        CountryEnum.from_raw(None)


# -------------------- TEST STATE_ENUM --------------------


@pytest.mark.unit
def test_stateenum_valid():
    assert StateEnum.from_raw("SP") == StateEnum.SP
    assert StateEnum.from_raw("sp") == StateEnum.SP
    assert StateEnum.from_raw("rj") == StateEnum.RJ
    assert StateEnum.from_raw(" rj ") == StateEnum.RJ


@pytest.mark.unit
def test_stateenum_invalid_value():
    with pytest.raises(InvalidState):
        StateEnum.from_raw("SPP")
    with pytest.raises(InvalidState):
        StateEnum.from_raw("XX")
    with pytest.raises(InvalidState):
        StateEnum.from_raw(" ")


@pytest.mark.unit
def test_stateenum_invalid_type():
    with pytest.raises(InvalidState):
        StateEnum.from_raw(123)
    with pytest.raises(InvalidState):
        StateEnum.from_raw(None)
