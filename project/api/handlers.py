import logging

from aiohttp.web import json_response
from project.api.api_handlers.auth import BasicAuthMiddleware

# Handlers API CRUD
from project.api.api_handlers.crud.сhecking_requests import (
    check_query_create,
    check_query_delete,
    check_query_read,
    check_query_update,
    date_iso,
)

# Handlers DataBase CRUD
from project.api.db_handlers.crud.CREATE import create_user
from project.api.db_handlers.crud.DELETE import delete_user
from project.api.db_handlers.crud.READ import read_users
from project.api.db_handlers.crud.UPDATE import update_user

logger = logging.getLogger(__name__)
auth = BasicAuthMiddleware()


class handCrud:
    __slots__ = ()

    @staticmethod
    @auth.required
    async def hand_create(request):
        try:
            logger.info("start request CREATE")
            query = request.rel_url.query
            logger.debug(f"Query received {query}")
            session = request.app["session"]
            logger.debug(f"Session obj received {query}")
            # CHECK QUERY REL
            if await check_query_create(query) is False:
                return json_response({"status": 404})
            # CHECK DATE IN QUERY
            if await date_iso(query=query) is False:
                return json_response({"status": 404})
            # DATABASE
            if await create_user(session, query) is False:
                return json_response({"status": 404})
            # RESULT
            logger.info("end request CREATE")
            return json_response({"status": 200})
        except Exception as err:
            logger.exception(str(err))
            return json_response({"status": 500})
        finally:
            logger.info("end request CREATE")

    @staticmethod
    @auth.required
    async def hand_read(request):
        try:
            logger.info("start request READ")
            query = request.rel_url.query
            logger.debug(f"Query received {query}")
            session = request.app["session"]
            logger.debug(f"Session obj received {query}")
            # CHECK QUERY REL
            if await check_query_read(query) is False:
                return json_response({"status": 404})
            limit = int(query["limit"])
            response = await read_users(session, limit)
            if response is False:
                return json_response({"status": 404})
            return json_response(response)
        except Exception as err:
            logger.exception(str(err))
            return json_response({"status": 500})
        finally:
            logger.info("end request READ")

    @staticmethod
    @auth.required
    async def hand_update(request):
        try:
            logger.info("start request UPDATE")
            query = request.rel_url.query
            logger.debug(f"Query received {query}")
            session = request.app["session"]
            logger.debug(f"Session obj received {query}")
            # CHECK QUERY REL
            if await check_query_update(query) is False:
                return json_response({"status": 404})
            # CHECK DATE IN QUERY
            if await date_iso(query=query) is False:
                return json_response({"status": 404})
            # UPDATE USER
            if await update_user(session, query) is False:
                return json_response({"status": 404})
            return json_response({"status": 200})
        except Exception as err:
            logger.exception(str(err))
            return json_response({"status": 500})
        finally:
            logger.info("end request UPDATE")

    @staticmethod
    @auth.required
    async def hand_delete(request):
        try:
            logger.info("start request DELETE")
            query = request.rel_url.query
            logger.debug(f"Query received {query}")
            session = request.app["session"]
            logger.debug(f"Session obj received {query}")
            # CHECK QUERY REL
            if await check_query_delete(query) is False:
                return json_response({"status": 404})
            if await delete_user(session, query) is False:
                return json_response({"status": 404})
            return json_response({"status": 200})
        except Exception as err:
            logger.exception(str(err))
            return json_response({"status": 500})
        finally:
            logger.info("end request UPDATE")
