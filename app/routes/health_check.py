import falcon


class HealthCheck:
    async def on_get(self, _, resp):
        """Handles GET requests"""
        resp.status = falcon.HTTP_200  # pylint: disable=no-member
        resp.media = {"status": "ok"}
        return resp
