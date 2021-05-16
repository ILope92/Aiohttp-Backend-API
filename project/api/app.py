import logging

from aiohttp.web import Application
from aiohttp_swagger import setup_swagger
from project.api.routes import setup_routes
from project.api.settings_app import close_pg, init_pg, pg_args_settings
from project.settings.load_settings import Settings

logger = logging.getLogger(__name__)


def swagger_path():
    try:
        logger.info("Connect swagger_path")
        setting = Settings()
        path = setting.swagger_path()
        logger.debug(f"Got the path swagger: {path}")
        return path
    except Exception as err:
        logger.exception(str(err))


def create_app(conn_db=None) -> Application:
    try:
        logger.info("Getting started with app creation")
        app = Application()
        # Connect swagger doc
        setup_swagger(app=app, swagger_from_file=swagger_path(), swagger_url="/api/doc")
        logger.debug("setup swagger")
        # Setup routes
        setup_routes(app)
        # Connect and close database
        if isinstance(conn_db, bool):
            app.on_startup.append(init_pg)
        else:
            print(conn_db)
            app["settings_db"] = conn_db
            app.on_startup.append(pg_args_settings)
        app.on_cleanup.append(close_pg)
        logger.info("The app is built")
        return app
    except Exception as err:
        logger.exception(err)
