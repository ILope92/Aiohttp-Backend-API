import argparse
import os
import pathlib
import sys
from types import SimpleNamespace
from typing import Union

from configargparse import Namespace
from dotenv import load_dotenv

from alembic.config import CommandLine, Config

# path to migration scripts
__base_path__ = "project/db/alembic"


def config_alembic(cmd_opts: Union[Namespace, SimpleNamespace]) -> Config:
    config = Config(file_=cmd_opts.config, ini_section=cmd_opts.name, cmd_opts=cmd_opts)
    config.set_main_option("script_location", __base_path__)
    if cmd_opts.pg_url:
        config.set_main_option("sqlalchemy.url", cmd_opts.pg_url)
    return config


def main():
    BASE_DIR = pathlib.Path(__file__).parent.parent.parent
    load_dotenv(os.path.join(BASE_DIR, ".env"))
    sys.path.append(BASE_DIR)

    alembic = CommandLine()
    alembic.parser.formatter_class = argparse.ArgumentDefaultsHelpFormatter
    alembic.parser.add_argument(
        "--pg-url",
        default=os.environ["POSTGRES_HOST"],
        help="Database URL .env var: POSTGRES_HOST]",
    )

    options = alembic.parser.parse_args()
    if "cmd" not in options:
        alembic.parser.error("too few arguments")
        exit(128)
    else:
        config = config_alembic(options)
        exit(alembic.run_cmd(config, options))


if __name__ == "__main__":
    main()
