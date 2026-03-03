import logging
import os
from redis import Redis
from rq import Worker

from app.core.cache import redis_client
from app.core.queue import photo_queue
from app.core.exceptions.exception_handlers import move_to_dlq


def run_worker():
    redis: Redis = redis_client

    worker = Worker(
        queues=[photo_queue],
        connection=redis,
        name=f"photo-worker-{os.getpid()}",
        exception_handlers=[move_to_dlq],
    )
    worker.work(
        with_scheduler=True,
        logging_level=logging.INFO,
    )


if __name__ == "__main__":
    run_worker()
