from settings import config
from helpers.log_helper import get_logger
import requests as rq
import time
from random import randint

page_logger = get_logger(__name__)


class PG_Helper:
    __slots__ = ('res',)

    def __init__(self, source):
        delay = config.DELAY
        if isinstance(delay, list):
            time.sleep(randint(*delay))
        for _ in range(config.MAX_RETRIES):
            try:
                self.res = rq.get(source, headers=config.HEADERS, timeout=30, proxies=config.PROXIES)
                break
            except:
                time.sleep(randint(1, 5))
                page_logger.error(f'not connection to {source}')

    def __enter__(self):
        return self

    def get_text(self):
        try:
            return self.res.text
        except:
            return None

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val:
            raise
