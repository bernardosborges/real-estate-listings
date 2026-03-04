from fastapi import Depends
from sqlalchemy.orm import Session

from app.api.deps.general_deps import get_db_session
from app.infrastructure.db.unit_of_work.unit_of_work_sqlalchemy import (
    SQLAlchemyUnitOfWork,
)


def get_uow(db: Session = Depends(get_db_session)):
    uow = SQLAlchemyUnitOfWork(db)
    try:
        yield uow

    except Exception:
        uow.rollback()
        raise
