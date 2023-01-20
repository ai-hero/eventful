import sys
import httpx
import logging
from helpers.event_context import EventContext

# Set up logger
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)


def ensure_webhook(_: str, __: str, listener: dict):
    listener["sink"] = {"type": "webhook", "callback_url": listener["callback_url"]}
    # Need to add healthcheck to identify listeners.
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
    callback_url = listener["sink"]["callback_url"]
    try:
        with httpx.Client(headers=new_event.headers()) as client:
            resp = client.post(callback_url, json=payload)
            resp.raise_for_status()
    except httpx.HTTPError:
        logger.error(
            "ERROR:\tcallback\t!!!\t%s/%s -> %s",
            new_event.event_type,
            group,
            callback_url,
        )
