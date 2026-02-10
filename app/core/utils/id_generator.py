from nanoid import generate

ALPHABET = "abcdefghijklmnopqrstuvwxyz0123456789"


class IDGenerator:

    @staticmethod
    def generate_profile_public_id(size: int) -> str:
        return generate(ALPHABET, size=size)
    
    @staticmethod
    def generate_property_public_id(size: int) -> str:
        return generate(ALPHABET, size=size)