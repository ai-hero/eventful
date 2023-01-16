import re
import helpers.cache as cache_helper
from falcon import HTTPUnprocessableEntity  # pylint: disable=no-name-in-module

CHAINS = "chains"
UUID_PATTERN = re.compile(r"^[\da-f]{8}-([\da-f]{4}-){3}[\da-f]{12}$")


def get(chain_id: str) -> dict:
    return cache_helper.get(CHAINS, chain_id)


def push(chain_id: str, event_id: str, event_type: str, event_span: str, event_at):
    if not (isinstance(event_id, str) and UUID_PATTERN.match(event_id)):
        raise HTTPUnprocessableEntity("Bad _id.")
    if not isinstance(event_type, str):
        raise HTTPUnprocessableEntity("Bad 'type'.")
    if not isinstance(event_span, str):
        raise HTTPUnprocessableEntity("Bad 'span'.")

    # The chain event
    push_obj = {
        "_id": event_id,
        "type": event_type,
        "span": event_span,
        "at": event_at,
    }

    # Build an in-memory chain object
    chain = get(chain_id)
    chain.append(push_obj)
    cache_helper.put(CHAINS, chain_id, chain)
    return chain

    # @classmethod
    # def waiting_on(cls, trace_id: str, event_type: str, listener: dict):
    #     event_listeners = cache_helper.get("trace_waiters", trace_id)
    #     if not event_listeners:
    #         event_listeners = {}
    #     if event_type not in event_listeners:
    #         event_listeners[event_type] = []
    #     event_listeners[event_type].append(listener)
    #     cache_helper.put("trace_waiters", trace_id, listener)

    # @classmethod
    # def noitfy_trace_event(cls, trace_id: str, event_type: str):
    #     event_listeners = cache_helper.get("trace_waiters", trace_id)
    #     if event_listeners and event_type in event_listeners:
    #         listeners = event_listeners[event_type]
    #         print(f"Should notify: {listeners}")
