import json
import traceback
import falcon
import falcon.asgi
from functools import partial
from falcon import Request, Response, media
from helpers.encoder import CustomJsonEncoder
from routes.health_check import HealthCheck
from routes.one_event import OneEventRoute


async def custom_handle_uncaught_exception(
    req: Request, resp: Response, exception: Exception, _: dict
):
    traceback.print_exc()
    resp.status = falcon.HTTP_500
    resp.media = f"{exception}"


# falcon.asgi.App instances are callable ASGI apps...
# in larger applications the app is created in a separate file
app = falcon.asgi.App()
app.add_error_handler(Exception, custom_handle_uncaught_exception)

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
app.add_route("/v1/events/{event_id}", OneEventRoute)
