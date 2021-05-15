import logging
import re

logger = logging.getLogger(__name__)


def admin_actions(query_rel):
    if query_rel["login"] == "admin":
        logger.info("The admin tried to update his rights? No! You're the admin!")


async def check_query_create(query_rel):
    logger.debug("Start checking parameters /create")
    try:
        if len(query_rel) == 0:
            logger.debug("Error in the number of request parameters")
            return False

        check_keys = (
            "login",
            "password",
            "date_birth",
            "first_name",
            "last_name",
            "permission",
        )
        for i in check_keys:
            if i not in query_rel:
                logger.debug("Check for parameters in the request failed")
                return False
        # CHECK permission
        try:
            permission = int(query_rel[check_keys[-1]])
            if permission <= 2 and permission >= 0:
                logger.debug("Verification of the permission request is successful")
                return True
            else:
                logger.debug(
                    f"Permission request verification failed. permission: {permission}"
                )
                return False
        except KeyError:
            return False
        except ValueError:
            return False
        logger.debug("Request parameters checked")
        return True
    except Exception as err:
        logger.exception(str(err))


async def check_query_read(query_rel):
    logger.debug("Start checking parameters /read")
    try:
        if len(query_rel) == 0:
            logger.debug("Error in the number of request parameters")
            return False

        check_keys = "limit"
        if check_keys not in query_rel:
            logger.debug("Check for parameters in the request failed")
            return False
        logger.debug("All parameters are checked")
        return True
    except Exception as err:
        logger.exception(str(err))


async def check_query_update(query_rel):
    logger.debug("Start checking parameters /update")
    try:
        if len(query_rel) == 0:
            logger.debug("Error in the number of request parameters")
            return False

        check_keys = (
            "login",
            "password",
            "date_birth",
            "first_name",
            "last_name",
            "permission",
        )
        for i in check_keys:
            if i not in query_rel:
                logger.debug("Check for parameters in the request failed")
                return False
        # CHECK permission
        try:
            permission = int(query_rel[check_keys[-1]])
            if permission <= 2 and permission >= 0:
                logger.debug("Verification of the permission request is successful")
                return True
            else:
                logger.debug(
                    f"Permission request verification failed. permission: {permission}"
                )
                return False
        except KeyError:
            return False
        except ValueError:
            return False
        # admin
        if query_rel["login"] == "admin":
            logger.info(
                "The admin tried to update his permission? No! You're the admin!"
            )
            return False
        logger.debug("All parameters are checked")
        return True
    except Exception as err:
        logger.exception(str(err))


async def check_query_delete(query_rel):
    logger.debug("Start checking parameters /delete")
    try:
        if len(query_rel) == 0:
            logger.debug("Error in the number of request parameters")
            return False

        check_keys = "login"
        if check_keys not in query_rel:
            logger.debug("Check for parameters in the request failed")
            return False
        # admin
        if query_rel["login"] == "admin":
            logger.info("Is the admin trying to delete himself? Don't be ridiculous!")
            return False
        logger.debug("All parameters are checked")
        return True
    except Exception as err:
        logger.exception(str(err))


async def date_iso(query):
    logger.debug("Start checking date parameters")
    # check pattern ISO in date
    try:
        pattern = re.findall(r"\d{4}-\d{2}-\d{2}", query["date_birth"])
        if len(pattern) > 1:
            logger.debug("Error in the request, the date does not match the ISO format")
            return False
        res = pattern[0].split("-")
        # elem date in int type
        result = [int(i) for i in res]
        month = result[1]
        day = result[2]
        if month > 12:
            logger.debug(
                f"Error in the request, the month can not be more than 12.\
                    Meaning: {day}"
            )
            return False
        if day > 31:
            logger.debug(
                f"Error in the request, the day can not be more than 31.\
                    Meaning: {day}"
            )
            return False
        logger.debug("All parameters are checked")
        return True
    except IndexError:
        logger.debug("Error in the request, the date does not match the ISO format")
        return False
    except Exception as err:
        logger.exception(str(err))
