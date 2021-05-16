import logging

from aiohttp.web import run_app

from project.api.app import create_app
from project.log import loggers
from project.utils.args_parse import setup_args
from project.utils.environment import append_root_env

# Environment
append_root_env()

# Logger
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    # setup argparse
    args = setup_args()
    # setup logger
    loggers.setup_logger(args.debug)
    logger.info("start application")
    if args.no_env:
        app = create_app(conn_db=args.no_env)
    else:
        app = create_app(
            conn_db={
                "login": args.db_login,
                "password": args.db_password,
                "host": args.db_host,
                "port": args.db_port,
                "database": args.db_database,
            }
        )
    run_app(app, host=args.host, port=args.port)
