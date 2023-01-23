import sys
import logging
from datetime import datetime
import helpers.cache as cache_helper
import helpers.webhook as webhook_helper
import helpers.redis_queue as redis_queue_helper
from helpers.event_context import EventContext

# Set up logger
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)


class Subscriptions:
    @classmethod
    def subscribe(cls, event_type: str, group: str, listener: dict):
        listeners = cache_helper.get("event_subscribers", event_type)
        listener["at"] = datetime.utcnow()

        match listener["type"]:
            case "webhook":
                webhook_helper.ensure_webhook(event_type, group, listener)
            case "queue":
                redis_queue_helper.ensure_queue(event_type, group, listener)
        if listeners is None:
            listeners = {}
        listeners[group] = listener
        cache_helper.put("event_subscribers", event_type, listeners, None)
        logger.info("SUB:\t%s\t<--\t%s/%s", event_type, group, listener["type"])
        return listener

    @classmethod
    def trigger(
        cls, event_context: EventContext, event_type: str, payload: dict
    ) -> EventContext:
        logger.info(
            "TRIG:\t%s/%s\t-->\t%s/*",
            event_context.event_type,
            event_context.event_id,
            event_type,
        )
        listeners = cache_helper.get("event_subscribers", event_type)
        if listeners:
            new_event = event_context.next(event_type)

            for group, listener in listeners.items():
                try:
                    match listener["type"]:
                        case "webhook":
                            webhook_helper.forward(
                                new_event,
                                payload,
                                group,
                                listener,
                            )
                        case "queue":
                            redis_queue_helper.forward(
                                new_event,
                                payload,
                                group,
                                listener,
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
