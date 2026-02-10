from rq import Retry

from app.core.queue import photo_queue
from app.jobs.photo_job import process_uploaded_photo_job

def enqueue_photo_processing(photo_public_id: str) -> None:
    photo_queue.enqueue(
        process_uploaded_photo_job,
        photo_public_id,
        retry = Retry(max=3, interval=[10, 30, 60]),
        job_timeout = 300
    )