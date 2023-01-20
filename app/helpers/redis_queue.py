import os
import sys
import redis
import logging
from bson.json_util import dumps
from helpers.event_context import EventContext

REDIS_CONNECTION_STRING = os.environ["REDIS_CONNECTION_STRING"]
EVENTFUL_TOPIC = "eventful"
EVENTFUL_CONNECTION_STRING = f"{REDIS_CONNECTION_STRING}/{EVENTFUL_TOPIC}"
pool = redis.ConnectionPool.from_url(EVENTFUL_CONNECTION_STRING)

# Set up logger
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)


def ensure_queue(event_type: str, group: str, listener: dict):
    listener["sink"] = {
        "type": "redis",
        "connection_string": EVENTFUL_CONNECTION_STRING,
        "topic": f"{event_type}___{group}",
    }
    return listener


def forward(
    new_event: EventContext,
    payload: dict,
    group: str,
    listener: dict,
):
    logger.info(
        "FWD:\t%s/%s\t-->\t%s/%s",
        new_event.event_type,
        new_event.event_id,
        group,
        listener["sink"]["type"],
    )
    try:
        redis_client = redis.StrictRedis(connection_pool=pool, decode_responses=True)
        redis_client.lpush(
            listener["sink"]["topic"],
            dumps(
                {"method": "event", "headers": new_event.headers(), "payload": payload}
            ),
        )
    except redis.exceptions.RedisError:
        logger.error(
            "ERROR:\tlpush\t!!!\t%s/%s",
            new_event.event_type,
            group,
        )
