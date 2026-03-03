import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import MetaData
from app.core.config import settings



# URL do db (psycopg v3)
SQLALCHEMY_DATABASE_URL = (
    f"postgresql+psycopg://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
)

naming_convention = {
    "ix": "ix_%(table_name)s_%(column_0_name)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}
metadata = MetaData(naming_convention=naming_convention)

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True) # Echo shows SQL commands on terminal for debugging
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base(metadata=metadata)

logger = logging.getLogger(__name__)

# Dependency
#@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    # Catching exceptions was moved to UnitOfWork
    # except SQLAlchemyError as e:
    #     db.rollback()
    #     logger.exception("Database error ocurred, rollback executed.")
    #     raise

    # except Exception as e:
    #     db.rollback()
    #     logger.exception("Unexpected error ocurred, rollback executed.")
    #     raise

    finally:
        db.close()
