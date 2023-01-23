import re
import helpers.cache as cache_helper

EVENT_STATE = "event_state"
UUID_PATTERN = re.compile(r"^[\da-f]{8}-([\da-f]{4}-){3}[\da-f]{12}$")


def get_state(event_id: str) -> dict:
    event_state = cache_helper.get(EVENT_STATE, event_id)
    if event_state is not None and event_state["state"] in ["done", "error"]:
        cache_helper.put(EVENT_STATE, event_id, event_state, expires=60)
    return event_state


def put_state(event_id: str, event_state: dict):
    cache_helper.put(EVENT_STATE, event_id, event_state)
    return event_state
