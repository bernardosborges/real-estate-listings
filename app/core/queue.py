from redis import Redis
from rq import Queue

from app.core.cache import redis_client

redis: Redis = redis_client

photo_queue = Queue(
    name="photo-processing",
    connection=redis,
    default_timeout=300,
)

photo_dlq = Queue(
    name="photo-dlq",
    connection=redis,
)
