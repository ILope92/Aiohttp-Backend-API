# Logger
import logging

from project.db.models import Right, User

logger = logging.getLogger(__name__)


async def create_user(session, query_rel):
    logger.debug("Start of a query to the database")

    # open session
    try:
        with session() as session:
            with session.begin():
                if await _login_exist(session, query_rel) is False:
                    return False
            id_user = await _add_user(session, query_rel)
            logger.debug(f"Last User ID received: {id_user.id}")
            await _add_permission(session, id_user.id, query_rel)
            session.commit()
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
        session.flush()
        return newUser
    except Exception as err:
        logger.exception(str(err))


async def _add_permission(session, user_id, query_rel):
    logger.debug("Adding user permission to the database")
    try:
        # add permission users in table rights
        logger.debug(
            f"Add permission: {user_id}, permission: {query_rel['permission']}"
        )
        newRight = Right(user_id=user_id, permission=query_rel["permission"])
        session.add(newRight)
        session.flush()
    except Exception as err:
        logger.exception(str(err))
