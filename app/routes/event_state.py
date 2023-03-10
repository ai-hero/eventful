import falcon
from falcon import Request, Response
import helpers.event_state as events_state_helper
from datetime import datetime


class EventStateRoute:
    def on_get(self, _: Request, resp: Response, event_id: str) -> Response:
        """Handles GET requests"""
        resp.status = falcon.HTTP_200  # pylint: disable=no-member
        resp.media = events_state_helper.get_state(event_id)
        return resp

    def on_post(self, req: Request, resp: Response, event_id: str) -> Response:
        """Handles POST requests"""
        event_state: dict = req.get_media()

        event_state["updated_at"] = datetime.utcnow()
        if "state" in event_state:
            state = event_state["state"]
            event_state[f"{state}_at"] = datetime.utcnow()
        resp.status = falcon.HTTP_200  # pylint: disable=no-member
        existing_state = events_state_helper.get_state(event_id)
        if existing_state:
            existing_state.update(event_state)
            event_state = existing_state
        events_state_helper.put_state(event_id, event_state)
        resp.media = event_state
        return resp
