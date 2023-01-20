import falcon
from falcon import Request, Response
from helpers.subscriptions import Subscriptions


class SubscribeRoute:
    def on_post(self, req: Request, resp: Response) -> Response:
        """Handles GET requests"""
        payload: list[dict] = req.get_media()
        listener = Subscriptions.subscribe(
            payload["type"], payload["group"], payload["listener"]
        )
        resp.status = falcon.HTTP_200  # pylint: disable=no-member
        resp.media = {
            "type": payload["type"],
            "group": payload["group"],
            "listener": listener,
        }
        return resp
