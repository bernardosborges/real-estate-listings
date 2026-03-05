from decimal import Decimal

from app.domain.entities.property import Property
from tests.factories.address_factory import address_factory


def property_factory(**overrides):
    def _create(**kwargs):
        data = {
            "id": 1,
            "public_id": "abc123abc123abc123abc",
            "profile_id": "user7",
            "description": "Apartamento padrão",
            "price": Decimal("50000.00"),
            "private_area": Decimal("80.00"),
            "is_active": True,
            "deleted_at": None,
            "address": address_factory()(),
        }

        data.update(overrides)
        data.update(kwargs)

        return Property(**data)

    return _create
