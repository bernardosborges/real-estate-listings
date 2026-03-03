from decimal import Decimal

from app.application.dto.address.address_input import AddressInput


class CreatePropertyInput:

    def __init__(
        self,
        description: str,
        price: Decimal,
        private_area: Decimal,
        address: AddressInput,
    ):

        self.description = description
        self.price = price
        self.private_area = private_area
        self.address = address
