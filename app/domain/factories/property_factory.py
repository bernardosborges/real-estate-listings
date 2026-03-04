from __future__ import annotations
from decimal import Decimal

from app.core.utils.id_generator import IDGenerator
from app.domain.entities.property import Property
from app.domain.entities.address import Address
from app.domain.value_objects.property.price import Price
from app.domain.value_objects.property.private_area import PrivateArea
from app.domain.value_objects.property.property_public_id import PropertyPublicId
from app.domain.constants.property_constants import PROPERTY_PUBLIC_ID_SIZE


class PropertyFactory:

    @classmethod
    def create_for_profile(
        cls,
        *,
        profile_id: int,
        address: Address,
        description: str,
        price: Decimal,
        private_area: Decimal,
    ) -> Property:

        raw_public_id = IDGenerator.generate_property_public_id(PROPERTY_PUBLIC_ID_SIZE)
        public_id = PropertyPublicId.from_raw(raw_public_id)

        price_vo = Price.from_raw(price)
        private_area_vo = PrivateArea.from_raw(private_area)

        return Property(
            id=None,
            public_id=public_id,
            profile_id=profile_id,
            address=address,
            description=description,
            price=price_vo,
            private_area=private_area_vo,
            is_active=True,
            deleted_at=None,
        )
