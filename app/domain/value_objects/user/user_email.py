from __future__ import annotations
import re
from app.domain.exceptions.user_exceptions import InvalidEmail

EMAIL_REGEX = re.compile(r'^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,63}$')

class UserEmail(str):

    @classmethod
    def from_raw(cls, value: str) -> str:
        normalized = cls._normalize(value)
        cls._validate(normalized)
        
        return cls(normalized)


    @staticmethod
    def _normalize(value: str) -> str:
        return value.strip().lower()
    

    @staticmethod
    def _validate(value: str) -> None:
        if not EMAIL_REGEX.fullmatch(value):
            raise InvalidEmail(value)