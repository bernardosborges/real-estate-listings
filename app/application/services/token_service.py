from abc import ABC, abstractmethod


class TokenService(ABC):

    @abstractmethod
    def generate(self, subject: str) -> dict:
        pass

    @abstractmethod
    def decode(self, token: str) -> dict:
        pass

