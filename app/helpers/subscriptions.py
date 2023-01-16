import sys
import logging
import httpx
from datetime import datetime
import helpers.cache as cache_helper
from helpers.events import EventContext

# Set up logger
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)


class Subscriptions:
    @classmethod
    def subscribe(cls, event_type: str, group: str, listener: dict):
        listeners = cache_helper.get("event_subscribers", event_type)
        listener["at"] = datetime.utcnow()
        if listeners is None:
            listeners = {}
        listeners[group] = listener
        cache_helper.put("event_subscribers", event_type, listeners, None)

    @classmethod
    def notify_event(cls, event_context: EventContext, event_type: str, payload: dict):
        listeners = cache_helper.get("event_subscribers", event_type)
        if listeners:
            new_event = event_context.next(event_type)
            for group, listener in listeners.items():
                try:
                    match listener["type"]:
                        case "webhook":
                            callback_url = listener["callback_url"]
                            try:
                                with httpx.Client(
                                    headers=new_event.headers()
                                ) as client:
                                    resp = client.post(callback_url, json=payload)
                                    resp.raise_for_status()
                            except httpx.HTTPError:
                                logger.error(
                                    "%s.%s: Cannot callback '%s'",
                                    event_type,
                                    group,
                                    callback_url,
                                )
                        case _:
                            logger.error(
                                "%s.%s: Unknown listener type '%s'",
                                event_type,
                                group,
                                listener["type"],
                            )
                except KeyError:
                    logger.error(
                        "%s.%s: SHOULD NOT HAPPEN: some attributes are missing for listener '%s'",
                        event_type,
                        group,
                        listener["type"],
                    )

            return new_event
        else:
            return None
