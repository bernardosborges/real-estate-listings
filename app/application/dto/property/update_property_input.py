from decimal import Decimal

from app.application.dto.address.update_address_input import UpdateAddressInput


class UpdatePropertyInput:

    def __init__(
        self,
        description: str | None = None,
        price: Decimal | None = None,
        private_area: Decimal | None = None,
        address: UpdateAddressInput | None = None,
    ):

        self.description = description
        self.price = price
        self.private_area = private_area
        self.address = address
