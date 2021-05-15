# Logger
import logging

from project.db.models import Right, User

logger = logging.getLogger(__name__)


async def create_user(session, query_rel):
    logger.debug("Start of a query to the database")

    # You need to make a session without begin()
    # and use flush () to get the id of the object being created
    # open session
    try:
        with session(autoflush=False) as session:
            with session.begin():
                if await _login_exist(session, query_rel) is False:
                    return False
                await _add_user(session, query_rel)
                user_id = await _last_id(session)
                await _add_permission(session, user_id, query_rel)
                logger.debug("Start of a query to the database")
                return True
    except Exception as err:
        logger.exception(str(err))


async def _login_exist(session, query_rel):
    logger.debug("Search for a login in the database")
    try:
        # search login
        query = session.query(User).filter(User.login == query_rel["login"]).first()
        if query is None:
            return True
        return False
    except Exception as err:
        logger.exception(str(err))


async def _add_user(session, query_rel):
    logger.debug("adding a user to the database")
    try:
        # add user in table users
        newUser = User(
            first_name=query_rel["first_name"],
            last_name=query_rel["last_name"],
            login=query_rel["login"],
            password=query_rel["password"],
            date_birth=query_rel["date_birth"],
        )
        session.add(newUser)
    except Exception as err:
        logger.exception(str(err))


async def _add_permission(session, user_id, query_rel):
    logger.debug("Adding user permission to the database")
    try:
        # add permission users in table rights
        newRight = Right(user_id=user_id, permission=query_rel["permission"])
        session.add(newRight)
    except Exception as err:
        logger.exception(str(err))


async def _last_id(session):
    logger.debug("Getting the last user id")
    try:
        # Getting the last user id
        last_id = session.query(User).order_by(User.id.desc()).first()
        if last_id is not None:
            return last_id.id + 1
        else:
            return 0
    except Exception as err:
        logger.exception(str(err))
