import argparse
import logging
import os
import sys

from aiohttp.web import run_app
from dotenv import load_dotenv

from project.api.app import create_app
from project.logs import loggers


# Environment
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))
sys.path.append(BASE_DIR)

# Logger
logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser()
# app args
parser.add_argument(
    "-H",
    "--host",
    help="Enter the ip of the server on which it will be launched, only the string is accepted: '0.0.0.0'",
    type=str,
    default="0.0.0.0",
)
parser.add_argument(
    "-P",
    "--port",
    help="Enter the port of the server on which it will run: port 3000",
    type=int,
    default=3000,
)
parser.add_argument(
    "-D", "--debug", help="on debug mode True | default: False", action="store_true"
)
# database args
parser.add_argument(
    "--no_env",
    help="By explicitly specifying the --no_env flag, you will not use the. env settings.",
    action="store_false",
)
parser.add_argument("--db_login", help="login in database", type=str, default="admin")
parser.add_argument(
    "--db_password", help="password in database", type=str, default="admin"
)
parser.add_argument("--db_host", help="host database", type=str, default="0.0.0.0")
parser.add_argument("--db_port", help="port database", type=int, default=5442)
parser.add_argument(
    "--db_database", help="select database", type=str, default="simalend"
)
args = parser.parse_args()

if __name__ == "__main__":
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
