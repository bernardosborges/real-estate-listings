from typing import Protocol

from app.domain.repositories.user_repository import UserRepository
from app.domain.repositories.user_profile_repository import UserProfileRepository
from app.domain.repositories.property_repository import PropertyRepository
from app.domain.repositories.address_repository import AddressRepository


class UnitOfWork(Protocol):
    user_repository: UserRepository
    profile_repository: UserProfileRepository
    property_repository: PropertyRepository
    address_repository: AddressRepository


    def commit(self) -> None: ...

    def rollback(self) -> None: ...

    def flush(self) -> None: ...
