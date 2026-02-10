from __future__ import annotations
import enum

from app.domain.exceptions.address_exceptions import InvalidState, InvalidCountry

class CountryEnum(str, enum.Enum):
    BR = "BR"

    @classmethod
    def from_raw(cls, value: str) -> CountryEnum:
        if not isinstance(value, str):
            raise InvalidCountry(f"Invalid value: {value}")

        try:
            return cls(value.strip().upper())
        except ValueError:
            raise InvalidCountry(f"Unknown country: {value}")


class StateEnum(str, enum.Enum):
    AC = "AC"
    AL = "AL"
    AP = "AP"
    AM = "AM"
    BA = "BA"
    CE = "CE"
    DF = "DF"
    ES = "ES"
    GO = "GO"
    MA = "MA"
    MT = "MT"
    MS = "MS"
    MG = "MG"
    PA = "PA"
    PB = "PB"
    PR = "PR"
    PE = "PE"
    PI = "PI"
    RJ = "RJ"
    RN = "RN"
    RS = "RS"
    RO = "RO"
    RR = "RR"
    SC = "SC"
    SP = "SP"
    SE = "SE"
    TO = "TO"

    @classmethod
    def from_raw(cls, uf: str) -> StateEnum:
        if not isinstance(uf, str):
            raise InvalidState(f"Invalid UF value: {uf}")
        
        try:
            return cls(uf.strip().upper())
        except ValueError:
            raise InvalidState(f"Unknown UF: {uf}")