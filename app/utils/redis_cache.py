import redis
import os

redis_client = redis.StrictRedis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    decode_responses=True
)

def set_cache(key: str, value: str, expire: int = 300):
    redis_client.set(key, value, ex=expire)

def get_cache(key: str):
    return redis_client.get(key)

def delete_cache(key: str):
    redis_client.delete(key)