from helpers import CTGR_Helper, PRD_Helper, PG_Helper
import csv


class CategoryParser:
    articul_set = set()
    barcode_set = set()

    def __init__(self, source: str):
        self.source = source

    def __enter__(self):
        print('***')
        print('starting category parsing')
        with open('out/positions.csv', 'w', encoding='utf8', newline='') as output_file:
            dict_writer = csv.DictWriter(
                output_file,
                delimiter=";",
                fieldnames=PRD_Helper.futures,
                quoting=csv.QUOTE_NONE
            )
            dict_writer.writeheader()
        return self

    def parse_category(self, href_set: set):
        for href in href_set:
            print(f'==== start parsing catalog {href} ====')
            href = self.source[:-1] + href + '?pc=60'
            html = PG_Helper(href).get_text()
            cat_parser = CTGR_Helper(html)
            cat_page_count = int(cat_parser.get_page_count(selector='div.navigation a'))
            print(f'catalog contains {cat_page_count+1} pages')
            self.parse_cat_page(href)
            if cat_page_count:
                for page_num in range(2, cat_page_count + 1):
                    self.parse_cat_page(href, page_num)

    def parse_cat_page(self, href, page_num=1):
        html = PG_Helper(href + '&PAGEN_1=' + str(page_num)).get_text()
        cat_parser = CTGR_Helper(html)
        cat_parser.get_href_set_prod(selector='div.catalog-section a.name')
        if cat_parser.get_href_set():
            print(f'start parsing {page_num} page: ', href)
            for href in cat_parser.get_href_set():
                positions = [product for product in self.parse_prod(href)]
                print(positions)
                self.save_csv(positions)
            print(f'parsing page № {page_num} is completed')
        else:
            print('page is empty: ', href)

    def parse_prod(self, href):
        html = PG_Helper(self.source[:-1] + href).get_text()
        product_helper = PRD_Helper(html)
        product_helper.sku_link = self.source + href
        for product in product_helper.get_prod(selector='div.catalog-element-top'):
            self.barcode_set.add(product['sku_barcode'])
            self.barcode_set.add(product['sku_article'])
            if (product['sku_barcode'] in self.barcode_set) and (product['sku_article'] in self.articul_set):
                continue
            yield product

    def save_csv(self, positions):
        with open('out/positions.csv', 'a', encoding='utf8', newline='') as output_file:
            dict_writer = csv.DictWriter(
                output_file,
                delimiter=";",
                fieldnames=PRD_Helper.futures,
                quoting=csv.QUOTE_NONE
            )
            dict_writer.writerows(positions)

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('categories parsing is completed')
        if exc_val:
            raise
