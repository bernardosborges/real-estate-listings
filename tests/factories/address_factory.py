from decimal import Decimal

from app.domain.entities.address import Address


def address_factory(**overrides):
    def _create(**kwargs):
        data = {
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

        data.update(overrides)
        data.update(kwargs)

        return Address(**data)
    return _create