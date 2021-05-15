import logging

from project.api.db_handlers.crud.create_response import Responses
from project.db.models import Right, User

logger = logging.getLogger(__name__)


async def read_users(session, limit):
    logger.debug("start of a read request to the database")
    try:
        # open session
        with session() as session:
            with session.begin():
                users, permissions = await _all_user(session, limit)
                if users is False:
                    return False
                return await Responses.read(users, permissions)
        return False
    except Exception as err:
        logger.exception(str(err))


async def _all_user(session, limit):
    logger.debug("Getting users")
    # search login
    try:
        user = session.query(User).order_by(User.id.desc()).limit(limit).all()
        permission = session.query(Right).order_by(Right.id.desc()).limit(limit).all()
        if user is not None and permission is not None:
            logger.debug("Users recived")
            return user, permission
        logger.warning("Explicit error in the database request")
        return False
    except Exception as err:
        logger.exception(str(err))
