import re
from app.domain.exceptions.user_profile_exceptions import InvalidProfilePublicId


PUBLIC_ID_REGEX = re.compile(r'^[a-z0-9_.]{4,30}$')

class UserProfilePublicId(str):

    @classmethod
    def from_raw(cls, value: str) -> str:
        normalized = cls._normalize(value)
        cls._validate(normalized)
        
        return cls(normalized)


    @staticmethod
    def _normalize(value: str) -> str:
        return value.strip().lower().replace("-", "_")
    

    @staticmethod
    def _validate(value: str) -> None:
        if not PUBLIC_ID_REGEX.fullmatch(value):
            raise InvalidProfilePublicId(value)
