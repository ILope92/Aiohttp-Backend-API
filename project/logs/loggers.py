import logging


_log_format = f"%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"


def setup_logger(mode):
    if mode is True:
        logging.basicConfig(
            level=logging.DEBUG,
            format=_log_format,
            handlers=[logging.FileHandler("logs/debug.log", mode='a'),
                      logging.StreamHandler()])
    else:
        logging.basicConfig(
            level=logging.INFO,
            format=_log_format,
            handlers=[logging.StreamHandler(),
                      get_file_handler()]
            )

def get_file_handler():
    file_handler = logging.FileHandler("logs/app.log")
    file_handler.setLevel(logging.WARNING)
    file_handler.setFormatter(logging.Formatter(_log_format))
    return file_handler

