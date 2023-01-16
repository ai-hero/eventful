import json
import traceback
import falcon
from functools import partial
from falcon import Request, Response, media
from helpers.encoder import CustomJsonEncoder
from routes.health_check import HealthCheck
from routes.event_state import EventStateRoute
from routes.subscribe import SubscribeRoute
from routes.trigger import TriggerRoute


def custom_handle_uncaught_exception(
    req: Request, resp: Response, exception: Exception, _: dict
):
    traceback.print_exc()
    resp.status = falcon.HTTP_500
    resp.media = f"{exception}"


app = falcon.App()
app.add_error_handler(Exception, custom_handle_Runcaught_exception)

# JSON Handler for the config
json_handler = media.JSONHandler(
    dumps=partial(json.dumps, cls=CustomJsonEncoder),
)
extra_handlers = {
    "application/json": json_handler,
}
app.req_options.media_handlers.update(extra_handlers)
app.resp_options.media_handlers.update(extra_handlers)

# Health Check
app.add_route("/", HealthCheck())
app.add_route("/v1/event/{event_id}/", EventStateRoute())
app.add_route("/v1/trigger/{event_type}", TriggerRoute())
app.add_route("/v1/subscribe", SubscribeRoute())
