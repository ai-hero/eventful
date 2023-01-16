import falcon
from falcon import Request, Response
from helpers.subscriptions import Subscriptions


class SubscribeRoute:
    def on_post(self, req: Request, resp: Response) -> Response:
        """Handles GET requests"""
        resp.status = falcon.HTTP_200  # pylint: disable=no-member
        listener: list[dict] = req.get_media()
        Subscriptions.subscribe(
            listener["type"], listener["group"], listener["listener"]
        )
        resp.media = {"success": True}
        return resp
