
import redis
from django.conf import settings

redis_client = redis.StrictRedis(
    host=getattr(settings, "REDIS_HOST", "127.0.0.1"),
    port=int(getattr(settings, "REDIS_PORT", 6379)),
    db=int(getattr(settings, "REDIS_DB", 0)),
    decode_responses=True,  
)
