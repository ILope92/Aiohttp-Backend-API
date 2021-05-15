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

# Argparse
parser = argparse.ArgumentParser()
parser.add_argument(
    "-H", "--host",
    help="Enter the ip of the server on which it will be launched, only the string is accepted: '0.0.0.0'",
    type=str, default='0.0.0.0')
parser.add_argument("-P", "--port", help="Enter the port of the server on which it will run", type=int, default=3000)
parser.add_argument("-D", "--debug", help="on debug mode True | default: False", type=bool, default=False)
args = parser.parse_args()

if __name__ == '__main__':
    loggers.setup_logger(args.debug)
    logger.info('start application')
    app = create_app()
    run_app(app, host=args.host, port=args.port)
