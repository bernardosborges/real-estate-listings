from functools import lru_cache

from app.core.database import get_db
from app.infrastructure.storage.s3_service import S3Service

# -----------------------------------------------
# DATABASE
# -----------------------------------------------


def get_db_session():
    yield from get_db()


# -----------------------------------------------
# STORAGE (S3)
# -----------------------------------------------


@lru_cache
def get_storage_service() -> S3Service:
    """
    S3 service dependecy.
    One instance per worker (cached)
    """
    return S3Service()
