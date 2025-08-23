import random
from common.redis_client import redis_client




CONFIRM_PREFIX = "confirm:"
TTL_SECONDS = 300

def _key(email: str) -> str:
    return f"{CONFIRM_PREFIX}{email.strip().lower()}"

def generate_confirmation_code(email: str) -> str:
    code = "".join(str(random.randint(0, 9)) for _ in range(6))
    redis_client.setex(_key(email), TTL_SECONDS, code)
    return code

def get_confirmation_code(email: str):
    return redis_client.get(_key(email))

def delete_confirmation_code(email: str):
    redis_client.delete(_key(email))

