from helpers.cfg_helper import CFG_helper
import requests as rq
import time
from random import randint


class PG_Helper:
    __slots__ = ('res',)

    def __init__(self, source):
        delay = CFG_helper().get_delay_range_s()
        if isinstance(delay, list):
            time.sleep(randint(*delay))
        for _ in range(CFG_helper().get_max_retries()):
            try:
                self.res = rq.get(source, headers=CFG_helper().get_headers())
                break
            except:
                print('not connection to ', source)

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
