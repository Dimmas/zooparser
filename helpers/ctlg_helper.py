from helpers.cfg_helper import CFG_helper
from bs4 import BeautifulSoup
import csv
import re


class CTLG_Helper:
    __slots__ = ('selector', 'ctlg', 'bs4')

    def __init__(
            self,
            html,
            selector: str = None
    ):
        self.selector = selector
        self.ctlg = None
        self.bs4 = BeautifulSoup(html, "html.parser")

    def __enter__(self):
        return self

    def get_catalog(
            self,
            subcatalog: str = None,
    ):
        if not subcatalog:
            try:
                self.ctlg = self.bs4.select(self.selector)
            except AttributeError:
                raise Exception(f'not fount root category by SCC-selector: {self.selector}')
        else:
            try:
                self.ctlg = self.bs4.find('a', attrs={'href': re.compile(f"\/{subcatalog}\/$")}).parent
                self.ctlg = self.ctlg.select('li')
            except AttributeError:
                raise Exception(f'not fount category by href: {subcatalog}')
        return self.ctlg

    def get_childs(self):
        href_set = set()
        if not self.ctlg:
            raise Exception("menu is not parsed")
        for li in self.ctlg:
            a = li.select('a')
            try:
                name = a[0].text.strip()
                href = a[0].get('href')
                if not href in href_set:
                    href_set.add(href)
                    yield name, href
            except IndexError:
                continue

    def get_childs_list(self):
        catalog = []
        for child_name, child_href in self.get_childs():
            if child_href[0] == '/':
                href = child_href[1:]
            if child_href[-1] == '/':
                href = child_href[:-1]
            path = href.split('/')
            catalog.append({'name': child_name, 'id': path[-1], 'parent_id': path[-2], 'href': child_href})
        return catalog

    @staticmethod
    def save_csv(catalog: dict):
        with open(f'{CFG_helper().get_output_directory()}/categories.csv', 'w', encoding='utf8', newline='') as output_file:
            dict_writer = csv.DictWriter(
                output_file,
                delimiter=";",
                fieldnames=catalog[0].keys(),
                quoting=csv.QUOTE_NONE
            )
            dict_writer.writeheader()
            dict_writer.writerows(catalog)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val:
            raise
