import re
from datetime import datetime
from helpers.common import retry_auto_reconnect, get_collection
from motor.motor_asyncio import AsyncIOMotorCollection
from pymongo import ReturnDocument
import helpers.cache as cache_helper
from falcon import HTTPUnprocessableEntity  # pylint: disable=no-name-in-module

TRACES = "traces"
traces_collection: AsyncIOMotorCollection = get_collection(TRACES)
UUID_PATTERN = re.compile(r"^[\da-f]{8}-([\da-f]{4}-){3}[\da-f]{12}$")


def create_indexes(f):
    @retry_auto_reconnect
    def func(*args, **kwargs):
        return f(*args, **kwargs)

    return func


@retry_auto_reconnect
async def get(trace_id: str) -> dict:
    cached = await cache_helper.get(TRACES, trace_id)
    if cached:
        return cached
    event = await traces_collection.find_one(trace_id)
    if event is None:
        return []
    await cache_helper.put(TRACES, trace_id, event)
    return event


@retry_auto_reconnect
@create_indexes
async def push(
    trace_id: str, event_id: str, event_type: str, event_span: str, event_at
):
    if not (isinstance(event_id, str) and UUID_PATTERN.match(event_id)):
        raise HTTPUnprocessableEntity("Bad event_id.")
    if not isinstance(event_type, str):
        raise HTTPUnprocessableEntity("Bad 'event_type'.")
    if not isinstance(event_span, str):
        raise HTTPUnprocessableEntity("Bad 'event_span'.")

    # The trace event
    push_obj = {
        "event_id": event_id,
        "event_type": event_type,
        "event_span": event_span,
        "event_at": event_at,
    }

    # Build an in-memory trace object
    trace = await get(trace_id)
    trace.append(push_obj)
    await cache_helper.put(TRACES, trace_id, trace)

    # Update the db
    insert_obj = {
        "_id": trace_id,
        "trace": [],
        "is_deleted": False,
        "created_at": datetime.utcnow(),
    }
    upsert_obj = {
        "$push": push_obj,
        "$inc": {"version": 1},
        "$setOnInsert": insert_obj,
    }
    traces_collection.find_one_and_update(
        {"_id": trace_id},
        upsert_obj,
        return_document=ReturnDocument.AFTER,
        upsert=True,
    )

    return trace
