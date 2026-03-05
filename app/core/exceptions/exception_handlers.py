import logging
import traceback
from fastapi import Request
from fastapi.responses import JSONResponse
from rq.job import Job

# from redis import Redis
from datetime import datetime, timezone

from app.core.exceptions.domain_exception import DomainException
from app.core.queue import photo_dlq

logger = logging.getLogger(__name__)


async def domain_exception_handler(request: Request, exc: DomainException):
    return JSONResponse(status_code=exc.status_code, content={"error": exc.error_code, "message": exc.message})


def move_to_dlq(job: Job, exc_type, exc_value, tb):

    try:
        job_args = job.args or []
        photo_public_id = job_args[0] if job_args else None

        payload = {
            "original_job_id": job.id,
            "func_name": job.func_name,
            "photo_public_id": photo_public_id,
            "exception_type": exc_type.__name__,
            "exception_message": str(exc_value),
            "traceback": "".join(traceback.format_tb(tb)),
            "failed_at": datetime.now(timezone.utc).isoformat(),
        }

        photo_dlq.enqueue("app.jobs.dlq.reprocess_dlq_job.handle_dlq_job", payload)

        logger.error(
            "Job moved to DLQ.",
            extra={"job_id": job.id, "photo_public_id": photo_public_id, "exception": exc_type.__name__},
        )

    except Exception:
        logger.error("Failed to move job moved to DLQ.")

    return False
