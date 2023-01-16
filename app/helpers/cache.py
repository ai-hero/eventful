import os
import redis
from bson.json_util import dumps, loads

REDIS_CONNECTION_STRING = os.environ["REDIS_CONNECTION_STRING"]
pool = redis.ConnectionPool.from_url(REDIS_CONNECTION_STRING)
EXPIRES = 1800  # enough time for services to come up


def put(obj_type: str, obj_id: str, obj: dict, expires=EXPIRES):
    redis_client = redis.StrictRedis(connection_pool=pool, decode_responses=True)
    key = f"{obj_type}__{obj_id}"
    redis_client.set(key, dumps(obj), ex=expires)


def delete(obj_type: str, obj_id: str):
    redis_client = redis.StrictRedis(connection_pool=pool, decode_responses=True)
    key = f"{obj_type}__{obj_id}"
    redis_client.delete(key)


def get(obj_type: str, obj_id: str):
    key = f"{obj_type}__{obj_id}"
    redis_client = redis.StrictRedis(connection_pool=pool, decode_responses=True)
    obj = redis_client.get(key)
    if obj:
        return loads(obj.decode("utf-8"))
    else:
        return None
