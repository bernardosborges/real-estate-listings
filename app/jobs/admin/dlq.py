from redis import Redis
from rq.job import Job

from app.core.cache import redis_client
from app.core.queue import photo_queue


def reprocess_dlq_job(job_id: str):

    redis: Redis = redis_client

    job = Job.fetch(job_id, connection=redis)
    photo_queue.enqueue(job.func, *job.args, **job.kwargs)
