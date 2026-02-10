from __future__ import annotations
from datetime import datetime, timezone
from decimal import Decimal

from app.domain.value_objects.property.property_public_id import PropertyPublicId
from app.domain.value_objects.property.price import Price
from app.domain.value_objects.property.private_area import PrivateArea
from app.domain.constants.property_constants import PROPERTY_DESCRIPTION_MAX_LENGHT
from app.domain.entities.address import Address
from app.domain.exceptions.property_exceptions import PropertyAlreadyActive, PropertyAlreadyDeactivated, PropertyCannotBeRestored, PropertyAlreadyDeleted


class Property:

    def __init__(
            self,
            id: int | None,
            public_id: str,
            profile_id: str,
            address: Address,
            description: str,
            price: Decimal,
            private_area: Decimal,
            is_active: bool,
            deleted_at: datetime | None,
    ):
        
        self.id = id
        self.profile_id = profile_id
        self.address = address
        self.description = description
        self.is_active = is_active
        self.deleted_at = deleted_at

        self.public_id = PropertyPublicId.from_raw(public_id)
        self.price = Price.from_raw(price)
        self.private_area = PrivateArea.from_raw(private_area)


# -----------------------------------------------
# LIFECYCLE
# -----------------------------------------------

    @property
    def is_deleted(self) -> bool:
        return self.deleted_at is not None

    def soft_delete(self) -> None:
        if self.is_deleted:
            raise PropertyAlreadyDeleted()
        self.deleted_at = datetime.now(timezone.utc)

    def restore(self) -> None:
        if self.deleted_at is None:
            raise PropertyCannotBeRestored()
        self.deleted_at = None

    def activate(self) -> None:
        if self.is_active:
            raise PropertyAlreadyActive()
        self.is_active = True

    def deactivate(self) -> None:
        if not self.is_active:
            raise PropertyAlreadyDeactivated()
        self.is_active = False
            


# -----------------------------------------------
# ?????
# -----------------------------------------------

    def update_basic_info(
            self,
            *,
            description: str | None = None,
            price: Decimal | None = None,
            private_area: Decimal | None = None
    ) -> None:
        
        if description is not None:
            if len(description) > PROPERTY_DESCRIPTION_MAX_LENGHT:
                raise ValueError("Description too long")
            self.description = description

        if price is not None:
            self.price = Price.from_raw(price)

        if private_area is not None:
            self.private_area = PrivateArea.from_raw(private_area)