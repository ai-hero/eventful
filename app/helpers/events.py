import re
import helpers.cache as cache_helper

EVENT_STATE = "event_state"
UUID_PATTERN = re.compile(r"^[\da-f]{8}-([\da-f]{4}-){3}[\da-f]{12}$")


def get_state(event_id: str) -> dict:
    return cache_helper.get(EVENT_STATE, event_id)


def put_state(event_id: str, event_state: dict):
    cache_helper.put(EVENT_STATE, event_id, event_state)
    return event_state

    # if not (isinstance(event_id, str) and UUID_PATTERN.match(event_id)):
    #     raise HTTPUnprocessableEntity("Bad event_id.")
    # if not ("type" in event and isinstance(event["type"], str)):
    #     raise HTTPUnprocessableEntity("Bad 'type' in event.")
    # if "span" in event and not isinstance(event["span"], str):
    #     raise HTTPUnprocessableEntity("Bad 'span' in event.")
    # elif "span" not in event:
    #     event["span"] = "default"
    # if "headers" in event and not isinstance(event["headers"], dict):
    #     raise HTTPUnprocessableEntity("Bad 'headers' in event.")

    # # if there is a dependent event,
    # if "on_event" in event:
    #     if not (
    #         isinstance(event["on_event"], str) and UUID_PATTERN.match(event["on_event"])
    #     ):
    #         raise HTTPUnprocessableEntity("Bad 'on_event' in event.")
    #     on_event = get(event["on_event"])
    #     if not on_event:
    #         raise HTTPUnprocessableEntity("Did not find 'on_event' in event.")
    #     event["trace_id"] = on_event["trace_id"]
    # else:
    #     event["trace_id"] = str(uuid4())  # starts a new trace
    # if "waiting_on" in event and not isinstance(event["waiting_on"], dict):
    #     raise HTTPUnprocessableEntity("Bad 'waiting_on' in event.")
    # event.update(
    #     {
    #         "_id": event_id,
    #         "is_deleted": False,
    #         "created_at": datetime.utcnow(),
    #     }
    # )
    # cache_helper.put(EVENT_STATE, event_id, event)
    # return event
