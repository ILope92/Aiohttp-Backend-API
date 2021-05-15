import logging

from aiohttp.web import Application
from project.api.handlers import handCrud

logger = logging.getLogger(__name__)


def setup_routes(app: Application):
    # Create / Read / Update / Delete
    try:
        logger.info("Add routes")
        app.router.add_get("/api/v1/create", handCrud.hand_create)
        app.router.add_get("/api/v1/read", handCrud.hand_read)
        app.router.add_get("/api/v1/update", handCrud.hand_update)
        app.router.add_get("/api/v1/delete", handCrud.hand_delete)
        logger.info("Routes built")
    except Exception as err:
        logger.exception(str(err))
