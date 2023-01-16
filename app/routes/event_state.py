import falcon
from falcon import Request, Response
import helpers.events as events_helper


class EventStateRoute:
    def on_get(self, _: Request, resp: Response, event_id: str) -> Response:
        """Handles GET requests"""
        resp.status = falcon.HTTP_200  # pylint: disable=no-member
        resp.media = events_helper.get_state(event_id)
        return resp
