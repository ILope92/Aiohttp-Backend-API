import logging

from project.api.db_handlers.crud.create_response import Responses
from project.db.models import Right, User

logger = logging.getLogger(__name__)


async def update_user(session, query_rel):
    logger.debug("start of a request to the database to update the user")
    # open session
    try:
        with session() as session:
            with session.begin():
                update = await _updater(session, query_rel)
                return update
    except Exception as err:
        logger.exception(str(err))


async def _updater(session, query_rel):
    try:
        logger.debug("start of a request")
        # search login and update data
        user = session.query(User).filter(User.login == query_rel["login"])
        if user.first().id is None:
            logger.debug("The user with this login was not found")
            return False
        permission = (
            session.query(Right)
            .filter(user.first().id == Right.user_id)
            .update(await Responses.update_right(query_rel), synchronize_session=False)
        )
        user = user.update(await Responses.update(query_rel), synchronize_session=False)
        if user is None or permission is None:
            logger.warning("Explicit error in the request")
            return False
        logger.debug("The user with this login has been updated")
        return True
    except Exception as err:
        logger.exception(str(err))
