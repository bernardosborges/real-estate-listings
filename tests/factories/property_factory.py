from decimal import Decimal

def property_payload_factory(**overrides):
    payload = {
        "description": "Apartamento padrão",
        "price": "50000.00",
        "private_area": "80.00",
        "address": "Rua das Flores, 520",
        "latitude": "-30.0346",
        "longitude": "-51.2177"
    }

    payload.update(overrides)
    return payload