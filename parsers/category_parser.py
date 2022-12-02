from concurrent.futures import ThreadPoolExecutor
from helpers import CTGR_Helper, PRD_Helper, PG_Helper, CFG_helper
import csv


class CategoryParser:
    hash = set()

    def __init__(self, source: str):
        self.source = source
        self.output_directory = CFG_helper().get_output_directory()

    def __enter__(self):
        print('***')
        print('starting category parsing')
        with open(f'{self.output_directory}/positions.csv', 'w', encoding='utf8', newline='') as output_file:
            dict_writer = csv.DictWriter(
                output_file,
                delimiter=";",
                fieldnames=PRD_Helper.futures,
                quoting=csv.QUOTE_NONE
            )
            dict_writer.writeheader()
        return self

    def parse_categories(self, href_set: set):
        def parse_category(href):
            print(f'==== start parsing category {href} ====')
            href = self.source[:-1] + href + '?pc=60'
            with PG_Helper(href) as pgh:
                html = pgh.get_text()
            if not html:
                print('not connection to ', href)
                return False
            with CTGR_Helper(html) as cat_parser:
                cat_page_count = int(cat_parser.get_page_count(selector='div.navigation a'))
            print(f'catalog contains {1 if cat_page_count == 0 else cat_page_count} pages')
            try:
                self.parse_cat_page(href)
            except:
                return False
            if cat_page_count:
                for page_num in range(2, cat_page_count + 1):
                    try:
                        self.parse_cat_page(href, page_num)
                    except:
                        continue

        delay = CFG_helper().get_delay_range_s()
        if isinstance(delay, list):
            with ThreadPoolExecutor(16) as exe:
                exe.map(parse_category, href_set, timeout=120)
        else:
            for href in href_set:
                parse_category(href)

    def parse_cat_page(self, href, page_num=1):
        with PG_Helper(href + '&PAGEN_1=' + str(page_num)) as pgh:
            html = pgh.get_text()
        if not html:
            raise Exception('not connection to ', href)
        with CTGR_Helper(html) as cat_parser:
            cat_parser.get_href_set_prod(selector='div.catalog-section a.name')
            if cat_parser.get_href_set():
                print(f'start parsing {page_num} page: ', href)
                for href in cat_parser.get_href_set():
                    try:
                        positions = [product for product in self.parse_prod(href)]
                    except:
                        continue
                    self.save_csv(positions)
                print(f'parsing page № {page_num} is completed')
            else:
                print('page is empty: ', href)

    def parse_prod(self, href):
        with PG_Helper(self.source[:-1] + href) as pgh:
            html = pgh.get_text()
        if not html:
            raise Exception('not connection to ', href)
        with PRD_Helper(html) as product_helper:
            product_helper.sku_link = self.source + href
            for product in product_helper.get_prod(selector='div.catalog-element-top'):
                if (product['sku_barcode'], product['sku_article']) in self.hash:
                    continue
                self.hash.add((product['sku_barcode'], product['sku_article']))
                print(f"  parsed position (articul={str(product['sku_article'])}, barcode={str(product['sku_barcode'])})")
                yield product

    def save_csv(self, positions):
        with open(f'{self.output_directory}/positions.csv', 'a', encoding='utf8', newline='') as output_file:
            dict_writer = csv.DictWriter(
                output_file,
                delimiter=";",
                fieldnames=PRD_Helper.futures,
                quoting=csv.QUOTE_NONE
            )
            dict_writer.writerows(positions)

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('parsing categories is completed')
        print(f' parsed {len(self.hash)} positions')
        if exc_val:
            raise
