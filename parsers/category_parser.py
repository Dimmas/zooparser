from concurrent.futures import ThreadPoolExecutor
from helpers import CTGR_Helper, PRD_Helper, PG_Helper, get_logger
from settings import config
import csv
import os

category_logger = get_logger(__name__)


class CategoryParser:
    hash = set()
    href_set = set()

    def __init__(self, source: str):
        self.source = source
        self.output_directory = config.OUT_DIR
        self.positions_html_dir = f'{self.output_directory}/positions_html/'
        list(map(os.unlink, (os.path.join(self.positions_html_dir, f) for f in os.listdir(self.positions_html_dir))))

    def __enter__(self):
        category_logger.info('*** starting category parsing ***')
        self.path = f'{self.output_directory}/positions.csv'
        try:
            with open(self.path, 'w', encoding='utf8', newline='') as output_file:
                dict_writer = csv.DictWriter(
                    output_file,
                    delimiter=";",
                    fieldnames=PRD_Helper.futures,
                    quoting=csv.QUOTE_NONE
                )
                dict_writer.writeheader()
        except Exception as e:
            raise Exception(f'can not write csv file: {e}')
        return self

    def parse_categories(self, href_set: set):
        """
        Парсит категории. Запускает parse_category(), которая определяет сколько страниц в категории
        и запускает self.parse_cat_page() для парсинга ссылок на товары с очередной странички категории.
        на товары
        :param href_set: множество категорий для парсинга
        :return:
        """
        def parse_category(href: str):
            category_logger.info(f'==== start parsing category {href} ====')
            href = self.source[:-1] + href + '?pc=60'
            with PG_Helper(href) as pgh:
                html = pgh.get_text()
            if not html:
                category_logger.error(f'not connection to {href}')
                return False
            with CTGR_Helper(html) as cat_parser:
                cat_page_count = int(cat_parser.get_page_count(selector='div.navigation a'))
            category_logger.info(f'catalog {href} contains {1 if cat_page_count == 0 else cat_page_count} pages')
            try:
                self.parse_cat_page(href)
            except:
                category_logger.error(f'can not to parse {href}')
                return False
            if cat_page_count:
                for page_num in range(2, cat_page_count + 1):
                    try:
                        self.parse_cat_page(href, page_num)
                    except:
                        category_logger.error(f'can not to parse {href}, page_num={page_num}')
                        continue

        delay = config.DELAY
        if not isinstance(delay, list):
            with ThreadPoolExecutor(16) as exe:
                exe.map(parse_category, href_set, timeout=30)
        else:
            for href in href_set:
                parse_category(href)

    def parse_cat_page(self, href, page_num=1):
        """
        Парсит ссылки на товары с очередной  странички категории (по 60 шт. на странице), вызывает self.parse_prod()
        для парсинга непостредственно товаров. Если ссылка на товар уже присутствует в множесте собранных товаров,
        то не парсит такой товар.
        :param href: ссылка на категорию
        :param page_num:номер очередной странички
        """
        cat_href = href + '&PAGEN_1=' + str(page_num)
        with PG_Helper(cat_href) as pgh:
            html = pgh.get_text()
        if not html:
            raise Exception('not connection to ', cat_href)
        with CTGR_Helper(html) as cat_parser:
            cat_parser.get_href_set_prod(selector='div.catalog-section a.name')
            if cat_parser.get_href_set():
                category_logger.info(f'start parsing {page_num} page: {cat_href}')
                for href in cat_parser.get_href_set():
                    if href not in self.href_set:
                        self.href_set.add(href)
                        try:
                            positions = [product for product in self.parse_prod(href)]
                        except:
                            category_logger.error(f'can not to parse {href}')
                            continue
                        try:
                            self.save_csv(positions)
                        except Exception as e:
                            category_logger.error(f'can not write csv file: {e}')
                category_logger.info(f'parsing completed for page № {page_num} of {cat_href}')
            else:
                category_logger.warning(f'page is empty: {cat_href}')

    def parse_prod(self, href):
        """
        Парсит страничку с товаром. Если и sku_barcode и sku_article уже есть в множестве, то не записывает позицию.
        :param href: ссылка на страничку с товаром
        """
        with PG_Helper(self.source[:-1] + href) as pgh:
            html = pgh.get_text()
        if not html:
            raise Exception('not connection to ', href)
        with PRD_Helper(html) as product_helper:
            product_helper.sku_link = self.source[:-1] + href
            for product in product_helper.get_prod(selector='div.catalog-element-top'):
                if not product:
                    continue
                if (product['sku_barcode'], product['sku_article']) in self.hash:
                    continue
                self.hash.add(product['sku_barcode'] + product['sku_article'])
                try:
                    self.save_html(
                        file_name=f"{self.positions_html_dir + product['sku_article'] + product['sku_barcode']}.html",
                        html=html
                    )
                except Exception as e:
                    category_logger.error(f'{e}')
                yield product

    def save_csv(self, positions):
        try:
            with open(self.path, 'a', encoding='utf8', newline='') as output_file:
                dict_writer = csv.DictWriter(
                    output_file,
                    delimiter=";",
                    fieldnames=PRD_Helper.futures,
                    quoting=csv.QUOTE_NONE,
                    quotechar='',
                    escapechar='\\'
                )
                dict_writer.writerows(positions)
        except Exception as e:
            raise Exception(f'can not write csv file: {e}')

    def save_html(self, file_name: str, html: str):
        try:
            with open(file_name, "w") as file:
                file.write(html)
        except Exception as e:
            raise Exception(f'can not write html file ({file_name}): {e}')

    def __exit__(self, exc_type, exc_val, exc_tb):
        category_logger.info('*** parsing categories is completed ***')
        category_logger.info(f'*** parsed {len(self.hash)} positions ***')
        if exc_val:
            raise
