from abc import ABC, abstractmethod
from app.domain.entities.user import User
from app.domain.value_objects.user. user_email import UserEmail

class UserRepository(ABC):

    @abstractmethod
    def refresh(self, user: User) -> User:
        pass

    @abstractmethod
    def save(self, user: User) -> User:
        pass

    @abstractmethod
    def get_by_id(self, user_id: int) -> User | None:
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> User | None:
        pass

    @abstractmethod
    def exists_by_email(self, email: UserEmail) -> bool:
        pass