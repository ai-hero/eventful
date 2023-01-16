import re
from uuid import uuid4
from datetime import datetime
import helpers.cache as cache_helper

EVENT_STATE = "event_state"
UUID_PATTERN = re.compile(r"^[\da-f]{8}-([\da-f]{4}-){3}[\da-f]{12}$")


class EventContext:
    def __init__(
        self,
        authorization_header: str,
        session_id: str,
        chain_id: str,
        span_id: str,
        event_type: str,
        event_id: str,
        event_at: str,
        previous: str,
    ) -> "EventContext":
        self.authorization_header: str = authorization_header
        self.session_id: str = session_id
        self.chain_id: str = chain_id
        self.span_id: str = span_id
        self.event_type: str = event_type
        self.event_id: str = event_id
        self.event_at: datetime = event_at
        self.previous: str = previous

    def next(self, event_type):
        return EventContext(
            self.authorization_header,
            self.session_id,
            self.chain_id,
            self.span_id,
            event_type,
            str(uuid4()),
            datetime.utcnow(),
            self.event_id,
        )

    def headers(self):
        headers = {}
        if self.authorization_header:
            headers["Authorization"] = self.authorization_header
        if self.session_id:
            headers["X-Eventful-Session"] = self.session_id
        if self.chain_id:
            headers["X-Eventful-Chain"] = self.chain_id
        if self.span_id:
            headers["X-Eventful-Span"] = self.span_id
        if self.event_type:
            headers["X-Eventful-Type"] = self.event_type
        if self.event_id:
            headers["X-Eventful-Event"] = self.event_id
        if self.event_at:
            headers["X-Eventful-At"] = self.event_at.isoformat()
        if self.previous:
            headers["X-Eventful-Previous"] = self.previous
        return headers


def get_context_from_http(req) -> EventContext:
    event_context = EventContext(
        authorization_header=req.headers.get("AUTHORIZATION", None),
        session_id=req.headers.get("X-EVENTFUL-SESSION", None),
        chain_id=req.headers.get("X-EVENTFUL-CHAIN", None),
        span_id=req.headers.get("X-EVENTFUL-SPAN", None),
        event_type=req.headers.get("X-EVENTFUL-TYPE", None),
        event_id=req.headers.get("X-EVENTFUL-EVENT", None),
        event_at=req.headers.get("X-EVENTFUL-AT", None),
        previous=req.headers.get("X-EVENTFUL-PREVIOUS", None),
    )
    if not event_context.chain_id:
        event_context.chain_id = str(uuid4())
    return event_context


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
