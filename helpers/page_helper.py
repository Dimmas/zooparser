import requests as rq


class PG_Helper:

    def __init__(self, source):
        self.res = rq.get(source)

    def get_text(self):
        return self.res.text
