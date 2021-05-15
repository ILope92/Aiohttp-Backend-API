import logging

from project.db.models import Right, User
from sqlalchemy import and_

logger = logging.getLogger(__name__)


async def autorization(request, login, password):
    logger.debug("Start autorization")
    session = request.app["session"]

    async def search_user(session):
        # search user
        logger.debug("Getting user objects and their rights")
        try:
            # find
            user = (
                session.query(User)
                .where(and_(User.login == login, User.password == password))
                .first()
            )
            if user is None:
                logger.debug("User not found")
                return False
            # search right user.id
            user_permission = (
                session.query(Right).where(Right.user_id == user.id).first()
            )
            # delete a user and their rights
            if user is not None and user_permission is not None:
                logger.debug("All user data found")
                return user_permission.permission
            else:
                logger.warning("Explicit error in the database request")
                False
        except Exception as err:
            logger.exception(str(err))
            return False

    try:
        # open session
        with session() as session:
            with session.begin():
                right = await search_user(session)
                if right is False:
                    return False
                logger.debug("data from the database is received")
                return right
    except Exception as err:
        logger.exception(str(err))
        return False
