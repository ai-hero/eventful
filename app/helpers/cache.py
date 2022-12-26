import os
import aioredis
from bson.json_util import dumps, loads

REDIS_URL = os.environ["REDIS_URL"]
redis_client = aioredis.from_url(REDIS_URL)
EXPIRES = 300  # 5 minutes


async def put(obj_type: str, obj_id: str, obj: dict, expires=EXPIRES):
    key = f"{obj_type}__{obj_id}"
    await redis_client.set(key, dumps(obj), ex=expires)


async def delete(obj_type: str, obj_id: str):
    key = f"{obj_type}__{obj_id}"
    await redis_client.delete(key)


async def get(obj_type: str, obj_id: str):
    key = f"{obj_type}__{obj_id}"
    obj = await redis_client.get(key)
    if obj:
        return loads(obj.decode("utf-8"))
    else:
        return None
