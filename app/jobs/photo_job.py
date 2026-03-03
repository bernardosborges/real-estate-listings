import logging
from dataclasses import dataclass
from redis import Redis

from app.api.deps.general_deps import get_db_session, get_storage_service
from app.core.cache import redis_client
from app.infrastructure.storage.s3_service import S3Service
from app.services.photo_processing_service import PhotoProcessingService

logger = logging.getLogger(__name__)

LOCK_TIMEOUT = 300  # seconds

# -----------------------------------------------
# JOB
# -----------------------------------------------


def process_uploaded_photo_job(photo_public_id: str) -> None:
    logger.info("Starting photo processing job...", extra={"photo": photo_public_id})
    redis: Redis = redis_client

    lock = redis.lock(
        name=f"photo:lock:{photo_public_id}",
        timeout=LOCK_TIMEOUT,
        blocking=False,
    )

    if not lock.acquire():
        logger.info("Job skipped - already locked", extra={"photo": photo_public_id})
        redis.incr("metrics:photo.jobs.skipped")
        return

    try:
        redis.incr("metrics:photo.jobs.started")

        with get_db_session() as db:
            storage: S3Service = get_storage_service()
            service = PhotoProcessingService(db=db, storage=storage, redis=redis)
            service.process(photo_public_id)

        redis.incr("metrics:photo.jobs.success")

    except:
        redis.incr("metrics:photo.jobs.failed")
        logger.exception(
            "Photo processing job failed.", extra={"photo": photo_public_id}
        )
        raise

    finally:
        if lock.locked():
            lock.release()
