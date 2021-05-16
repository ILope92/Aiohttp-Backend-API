import logging


logger = logging.getLogger(__name__)


class Responses:
    """
    Data handler from the database and sending response
    """

    __slots__ = ()

    @staticmethod
    async def read(user, permission):
        logger.debug("Create response api/read")
        try:
            response = {
                "users": {
                    u.id: {
                        "first_name": u.first_name,
                        "last_name": u.last_name,
                        "login": u.login,
                        "permission": r.permission,
                    }
                    for u, r in zip(user, permission)
                }
            }
        except Exception as err:
            logger.exception(str(err))
        logger.debug("response api/read ready")
        return response

    @staticmethod
    async def update(query_rel):
        logger.debug("Create response api/update in query")
        try:
            updates = {
                "first_name": query_rel["first_name"],
                "last_name": query_rel["last_name"],
                "login": query_rel["login"],
                "password": query_rel["password"],
                "date_birth": query_rel["date_birth"],
            }
        except Exception as err:
            logger.exception(str(err))
        logger.debug("response api/update ready")
        return updates

    @staticmethod
    async def update_right(query_rel):
        logger.debug("Create response api/update in query")
        try:
            updates = {"permission": query_rel["permission"]}
        except Exception as err:
            logger.exception(str(err))
        logger.debug("response api/update ready")
        return updates
