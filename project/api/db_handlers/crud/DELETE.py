import logging

from project.db.models import Right, User

logger = logging.getLogger(__name__)


async def delete_user(session, query_rel):
    logger.debug("Start deleting a user from the database")
    try:
        # open session
        with session() as session:
            with session.begin():
                delete = _query_db(session, query_rel)
                if delete is False:
                    return False
                logger.debug("The deletion was successful")
                return True
    except Exception as err:
        logger.exception(str(err))


async def _query_db(session, query_rel):
    # search user
    logger.debug("Getting user objects and their permission")
    try:
        user = await session.query(User).where(User.login == query_rel["login"]).first()
        if user is None:
            logger.debug("User not found")
            return False
        # search right user.id
        permission = await session.query(Right).where(Right.user_id == user.id).scalar()
        # delete a user and their permission
        if user is not None and permission is not None:
            logger.debug("Deleting a user and their permission")
            session.delete(permission)
            session.delete(user)
        else:
            logger.warning("Explicit error in the database request")
            return False
    except Exception as err:
        logger.exception(str(err))
        return False
