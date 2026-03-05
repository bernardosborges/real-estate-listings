from __future__ import annotations
from datetime import datetime

from app.application.dto.address.address_output import AddressOutput


class PropertyListOutput:
    def __init__(
        self,
        public_id: str,
        profile_public_id: str | None,
        description: str,
        price: float,
        private_area: float,
        address: AddressOutput,
        is_active: bool,
        deleted_at: datetime | None = None,
    ):
        self.public_id = public_id
        self.profile_public_id = profile_public_id
        self.description = description
        self.price = price
        self.private_area = private_area
        self.address = address
        self.is_active = is_active
        self.deleted_at = deleted_at

    @classmethod
    def from_entity(cls, property, profile_public_id, is_publisher=False):

        if not is_publisher and not property.is_active:
            return None

        return cls(
            public_id=property.public_id,
            profile_public_id=profile_public_id,
            description=property.description,
            price=property.price.value,
            private_area=property.private_area.value,
            address=(AddressOutput.from_entity(property.address) if property.address else None),
            is_active=property.is_active,
            deleted_at=property.deleted_at,
        )
