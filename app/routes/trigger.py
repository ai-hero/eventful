import falcon
from falcon import Request, Response
from helpers.subscriptions import Subscriptions
from helpers.event_context import get_context_from_http
from helpers.event_state import get_state


class TriggerRoute:
    def on_post(self, req: Request, resp: Response, event_type: str) -> Response:
        """Handles GET requests"""
        resp.status = falcon.HTTP_200  # pylint: disable=no-member
        payload: list[dict] = req.get_media()
        event_context = get_context_from_http(req)
        new_event = Subscriptions.trigger(event_context, event_type, payload)

        # event = events_helper.put(event_id, new_event)
        # chains_helper.push(
        #     chain_id=event["chain_id"],
        #     event_id=event_id,
        #     event_type=event["type"],
        #     event_span=event["span"],
        #     event_at=event["created_at"],
        # )
        # if "waiting_on" in event:
        #     chain_id = event["waiting_on"]["chain_id"]
        #     waiting_on_event_type = event["waiting_on"]["event_type"]
        #     waiting_on_listener = event["waiting_on"]["listener"]
        #     Subscriptions.waiting_on(
        #         chain_id, waiting_on_event_type, waiting_on_listener
        #     )
        if new_event:
            resp.set_headers(new_event.headers())
            resp.media = get_state(new_event.event_id)
        else:
            resp.media = {"success": False}
        return resp
