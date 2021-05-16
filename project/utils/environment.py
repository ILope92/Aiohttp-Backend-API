import os
import sys
import pathlib

from dotenv import load_dotenv


def append_root_env():
    # Environment '.'
    BASE_DIR = pathlib.Path(__file__).parent.parent.parent
    load_dotenv(os.path.join(BASE_DIR, ".env"))
    sys.path.append(BASE_DIR)
