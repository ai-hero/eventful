from uuid import uuid4
from datetime import datetime
import helpers.event_state as events_state_helper


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
        next_event = EventContext(
            self.authorization_header,
            self.session_id,
            self.chain_id,
            self.span_id,
            event_type,
            str(uuid4()),
            datetime.utcnow(),
            self.event_id,
        )
        events_state_helper.put_state(
            next_event.event_id,
            event_state={"state": "created", "progress": 0.0, "message": "Created."},
        )
        return next_event

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
