from bs4 import BeautifulSoup
import re


class CTGR_Helper:
    __slots__ = ('href_set', 'bs4', 'page_count')

    def __init__(
            self,
            html
    ):
        self.href_set = set()
        self.bs4 = BeautifulSoup(html, "html.parser")
        self.page_count = 0

    def __enter__(self):
        return self

    def get_page_count(self, selector):
        try:
            last_page_href = self.bs4.select(selector)[-1]['href']
            self.page_count = re.findall(r'PAGEN_1=(\d+)', last_page_href)[0]
        except:
            pass
        return self.page_count

    def get_href_set_prod(self, selector):
        prod_a = self.bs4.select(selector)
        self.href_set = {a['href'] for a in prod_a}

    def get_href_set(self):
        return self.href_set

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val:
            raise
