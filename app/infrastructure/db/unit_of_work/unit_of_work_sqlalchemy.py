from sqlalchemy.orm import Session

from app.application.unit_of_work.unit_of_work import UnitOfWork
from app.infrastructure.db.repositories.user_repository_sqlalchemy import (
    UserRepositorySQLAlchemy,
)
from app.infrastructure.db.repositories.user_profile_repository_sqlalchemy import (
    UserProfileRepositorySQLAlchemy,
)
from app.infrastructure.db.repositories.property_repository_sqlalchemy import (
    PropertyRepositorySQLAlchemy,
)
from app.infrastructure.db.repositories.address_repository_sqlalchemy import (
    AddressRepositorySQLAlchemy,
)


class SQLAlchemyUnitOfWork(UnitOfWork):

    def __init__(self, session: Session):
        self.session = session
        self.user_repository = UserRepositorySQLAlchemy(session)
        self.profile_repository = UserProfileRepositorySQLAlchemy(session)
        self.property_repository = PropertyRepositorySQLAlchemy(session)
        self.address_repository = AddressRepositorySQLAlchemy(session)

    def commit(self) -> None:
        self.session.commit()

    def rollback(self) -> None:
        self.session.rollback()

    def flush(self) -> None:
        self.session.flush()
