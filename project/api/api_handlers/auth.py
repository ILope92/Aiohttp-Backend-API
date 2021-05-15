import functools
import logging

from aiohttp import BasicAuth, hdrs, web
from aiohttp.web import middleware
from project.api.db_handlers import auth_db
from project.settings.load_settings import Settings

logger = logging.getLogger(__name__)


@middleware
class BasicAuthMiddleware:
    def parse_auth_header(self, request):
        
        logger.debug('Parse auth')
        auth_header = request.headers.get(hdrs.AUTHORIZATION)
        if not auth_header:
            return None
        try:
            auth = BasicAuth.decode(auth_header=auth_header)
        except ValueError:  # pragma: no cover
            auth = None
        logger.debug('Parse auth success')
        return auth

    async def authenticate(self, request, handler):
        auth = self.parse_auth_header(request)
        return (auth is not None and await self.check_credentials(
            request,
            auth.login,
            auth.password,
            handler))

    async def check_permission(self, handler, permission):
        logger.debug('We get the user permission to the function')
        try:
            check_settings = Settings().permissions['CRUD'][handler.__name__]
            logger.debug(f'permission to function {handler.__name__} = {permission}')
            return permission in check_settings
        except Exception as err:
            logger.exception(str(err))
            return False

    async def check_credentials(self, request, username, password, handler):
        if username is None and password is None:
            logger.debug('No login and password')
            return False
        # QUERY IN DATABASE
        auth = await auth_db.autorization(request, username, password)
        if auth is None:
            logger.debug('Authorization failed')
            return False
        else:
            permission = await self.check_permission(handler, auth)
            return permission

    def challenge(self):
        return web.Response(
            body=b'', status=401, reason='UNAUTHORIZED',
            headers={
                hdrs.WWW_AUTHENTICATE: 'Basic realm=""',
                hdrs.CONTENT_TYPE: 'text/html; charset=utf-8',
                hdrs.CONNECTION: 'keep-alive'
            }
        )

    def required(self, handler):
        #logger.info(f'Request for authentication to the function {handler.__name__}')
        @functools.wraps(handler)
        async def wrapper(*args):
            request = args[-1]
            response = await self.authenticate(request, handler)
            if response is True:
                logger.info(f'Access is given: {handler.__name__}')
                return await handler(*args)
            elif response is False:
                logger.warning(f'someone tries to get in and doesnt get out: {handler.__name__}')
                return self.challenge()
        return wrapper

    async def __call__(self, request, handler):
        if not self.force:
            return await handler(request)
        else:
            if await self.authenticate(request):
                return await handler(request)
            else:
                return self.challenge()
