import logging
import pathlib

import yaml

logger = logging.getLogger(__name__)


class Settings:
    BASE_DIR = pathlib.Path(__file__).parent
    __yaml__ = '.yaml'
    __responses__ = f"{BASE_DIR}/docs/responses/errors{__yaml__}"
    __swagger__ = f"{BASE_DIR}/docs/swagger/swagger{__yaml__}"
    __permissions__ = f"{BASE_DIR}/docs/permissions/permissions_crud{__yaml__}"

    def __init__(self):
        try:
            logger.info("start of settings")
            with open(self.__responses__, 'r') as f:
                logger.debug(f'open file {self.__responses__}')
                self.responses = yaml.safe_load(f)

            with open(self.__swagger__, 'r') as f:
                logger.debug(f'open file {self.__swagger__}')
                self.swagger = yaml.safe_load(f)

            with open(self.__permissions__, 'r') as f:
                logger.debug(f'open file {self.__permissions__}')
                self.permissions = yaml.safe_load(f)

            logger.info('end of settings')
        except Exception as e:
            logger.exception(str(e))

    @classmethod
    def swagger_path(cls):
        logger.debug(f'swagger path: {cls.__swagger__}')
        return cls.__swagger__
