import falcon
from falcon import Request, Response
import helpers.events as events_helper
import helpers.traces as traces_helper


class OneEventRoute:
    async def on_get(self, _: Request, resp: Response, event_id: str) -> Response:
        """Handles GET requests"""
        resp.status = falcon.HTTP_200  # pylint: disable=no-member
        resp.media = await events_helper.get(event_id)
        return resp

    async def on_post(self, req: Request, resp: Response, event_id: str) -> Response:
        """Handles GET requests"""
        resp.status = falcon.HTTP_200  # pylint: disable=no-member
        event: list[dict] = await req.get_media()
        event["headers"] = {}
        auth_header = req.get_header("Authorization", default=None)
        if auth_header:
            event["headers"]["Authorization"] = auth_header
        event = await events_helper.put(event_id, event)
        traces_helper.push(
            trace_id=event["trace_id"],
            event_id=event_id,
            event_type=event["type"],
            event_span=event["span"],
            event_at=event["created_at"],
        )
        resp.media = event
        return resp
