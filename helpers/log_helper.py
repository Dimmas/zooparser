import logging
from helpers import CFG_helper


def get_logger(module_name, console_silence=False):
    logger = logging.getLogger(module_name)
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(f"{CFG_helper().get_logs()}/{module_name}.log", mode='w')

    formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    if not console_silence:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    return logger
