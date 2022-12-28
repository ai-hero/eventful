import falcon
from falcon import Request, Response
from helpers.subscriptions import Subscriptions


class SubscribeRoute:
    async def on_post(self, req: Request, resp: Response, event_id: str) -> Response:
        """Handles GET requests"""
        resp.status = falcon.HTTP_200  # pylint: disable=no-member
        payload: list[dict] = await req.get_media()
        event_type = payload["event_type"]
        listener = payload["listener"]
        Subscriptions.subscribe(event_type, listener)
        resp.media = {"status": "ok"}
        return resp
