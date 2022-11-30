from bs4 import BeautifulSoup
from enums import Tags, Futures
import csv
import re


class CTLG_Helper:

    def __init__(
            self,
            html,
            tag: Tags = None,
            future: Futures = None,
            future_name: str = None
    ):
        self.tag = tag
        self.future = future
        self.future_name = future_name
        self.ctlg = None
        self.bs4 = BeautifulSoup(html, "html.parser")

    def get_catalog(
            self,
            node: str = 'root',
    ):
        if node == 'root':
            try:
                selector = f'{self.__construct_selector__()} ul li.lev1'
                self.ctlg = self.bs4.select(selector)
            except AttributeError:
                exit(f'not fount root category by SCC-selector: {selector}')
        else:
            try:
                self.ctlg = self.bs4.find('a', attrs={'href': re.compile(f"{node}$")}).parent
                self.ctlg = self.ctlg.select('ul')
                print(self.ctlg)
                # не цепляет корневой каталог Хорьки
            except AttributeError:
                exit(f'not fount category by href: {node}')
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
                child_href = child_href[1:]
            if child_href[-1] == '/':
                child_href = child_href[:-1]
            path = child_href.split('/')
            entity = {'name': child_name, 'id': path[-1], 'parent_id': path[-2]}
            catalog.append(entity)
        return catalog

    @staticmethod
    def save_catalog(catalog: dict):
        with open('csv/categories.csv', 'w', encoding='utf8', newline='') as output_file:
            dict_writer = csv.DictWriter(
                output_file,
                delimiter=";",
                fieldnames=catalog[0].keys(),
                quoting=csv.QUOTE_NONE
            )
            dict_writer.writeheader()
            dict_writer.writerows(catalog)

    def __construct_selector__(self):
        selector = ''
        if self.tag:
            selector += self.tag
        if self.future:
            selector += self.future + self.future_name
        return selector
