import re
from uuid import uuid4
from datetime import datetime
from helpers.common import retry_auto_reconnect, get_collection
from motor.motor_asyncio import AsyncIOMotorCollection
import helpers.cache as cache_helper
from falcon import HTTPUnprocessableEntity  # pylint: disable=no-name-in-module

events_collection: AsyncIOMotorCollection = get_collection("events")
UUID_PATTERN = re.compile(r"^[\da-f]{8}-([\da-f]{4}-){3}[\da-f]{12}$")

EVENTS = "events"


def create_indexes(f):
    @retry_auto_reconnect
    def func(*args, **kwargs):
        return f(*args, **kwargs)

    return func


@retry_auto_reconnect
async def get(event_id: str) -> dict:
    cached = await cache_helper.get(EVENTS, event_id)
    if cached:
        return cached
    event = await events_collection.find_one(event_id)
    if event is None:
        return None
    await cache_helper.put(EVENTS, event_id, event)
    return event


@retry_auto_reconnect
@create_indexes
async def put(event_id: str, event: dict):
    if not (isinstance(event_id, str) and UUID_PATTERN.match(event_id)):
        raise HTTPUnprocessableEntity("Bad event_id.")
    if not ("type" in event and isinstance(event["type"], str)):
        raise HTTPUnprocessableEntity("Bad 'type' in event.")
    if "span" in event and not isinstance(event["span"], str):
        raise HTTPUnprocessableEntity("Bad 'span' in event.")
    if "headers" in event and not isinstance(event["headers"], dict):
        raise HTTPUnprocessableEntity("Bad 'headers' in event.")
    if "on_event" in event:
        if not (
            isinstance(event["on_event"], str) and UUID_PATTERN.match(event["on_event"])
        ):
            raise HTTPUnprocessableEntity("Bad 'on_event' in event.")
        on_event = await get(event["on_event"])
        if not on_event:
            raise HTTPUnprocessableEntity("Did not find 'on_event' in event.")
        event["trace_id"] = on_event["trace_id"]
    else:
        event["trace_id"] = str(uuid4())  # starts a new trace
    if "waiting_on" in event and not isinstance(event["waiting_on"], dict):
        raise HTTPUnprocessableEntity("Bad 'waiting_on' in event.")
    event.update(
        {
            "_id": event_id,
            "is_deleted": False,
            "created_at": datetime.utcnow(),
        }
    )
    events_collection.insert_one(event)
    await cache_helper.put(EVENTS, event_id, event)
    return event
