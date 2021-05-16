import logging
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger(__name__)


async def init_pg(app):
    try:
        logger.info("Start of data base initialization")
        db_url = os.environ["POSTGRES_HOST"]
        logger.info(f"Connect to {db_url}")
        engine = create_engine(db_url)
        app["db"] = engine
        app["session"] = sessionmaker(bind=engine)
        logger.debug("end of database initialization")
    except Exception as err:
        logger.exception(str(err))


async def pg_args_settings(app):
    try:
        logger.info("Start of data base initialization")
        settings = app["settings_db"]
        db_url = "postgresql://{0}:{1}@{2}:{3}/{4}".format(
            settings["login"],
            settings["password"],
            settings["host"],
            settings["port"],
            settings["database"],
        )

        logger.info(f"Connect to {db_url}")
        engine = create_engine(db_url)
        app["db"] = engine
        app["session"] = sessionmaker(bind=engine)
        logger.debug("end of database initialization")
    except Exception as err:
        logger.exception(str(err))


async def close_pg(app):
    try:
        app["db"].dispose()
        logger.debug("Closing the database connection")
    except Exception as err:
        logger.exception(str(err))
