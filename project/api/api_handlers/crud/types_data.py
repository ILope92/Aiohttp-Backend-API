from datetime import datetime as dt

from project.logs import loggers


logger = loggers.get_logger(__name__)


def string_to_date(string: str):
    logger.debug('Start creating a string in a date object')
    try:
        date = dt.fromisoformat(string)
        if isinstance(date, dt):
            logger.debug(f'There are no errors in the line, return: {dt}')
            return date
        else:
            logger.debug('Error in the line representing the date')
            False
    except Exception as err:
        logger.debug(str(err))
        return False
