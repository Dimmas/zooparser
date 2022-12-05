from bs4 import BeautifulSoup
from datetime import datetime
from helpers import get_logger

prd_logger = get_logger(__name__, console_silence=True)


class PRD_Helper:
    __slots__ = ('bs4', 'sku_link')
    futures = (
        'price_datetime',
        'price',
        'price_promo',
        'sku_status',
        'sku_barcode',
        'sku_article',
        'sku_name',
        'sku_category',
        'sku_country',
        'sku_weight_min',
        'sku_volume_min',
        'sku_quantity_min',
        'sku_link',
        'sku_images'
    )

    def __init__(
            self,
            html
    ):
        self.bs4 = BeautifulSoup(html, "html.parser")

    def __enter__(self):
        return self

    def get_prod(self, selector):
        try:
            product_div = self.bs4.select_one(selector)
        except:
            prd_logger.error(f'product not found by selector: {selector} in {self.sku_link}')
            return False
        if not product_div:
            prd_logger.error(f'product not found by selector: {selector} in {self.sku_link}')
            return False
        try:
            sku_country = product_div.select_one('div.catalog-element-offer-left p').get_text().split(' ')[2]
            if sku_country[-1] == ',':
                sku_country = sku_country[:-1]
        except:
            prd_logger.warning(f'product sku_country not found in {self.sku_link}')
            sku_country = None

        try:
            sku_name = product_div.select_one('h1').get_text()
        except:
            prd_logger.warning(f'product sku_name not found in {self.sku_link}')
            sku_name = None

        try:
            sku_category = '|'.join([a.text for a in self.bs4.select('ul.breadcrumb-navigation li a')])
        except:
            prd_logger.warning(f'product sku_category not found in {self.sku_link}')
            sku_category = None

        try:
            positions_table = product_div.select_one('table').select('tr.b-catalog-element-offer')
        except:
            self.position_warning()
            return None

        price_datetime = datetime.today().strftime("%H.%M.%S %Y-%m-%d")

        try:
            sku_images = [a['href'] for a in product_div.select('div.catalog-element-offer-pictures a') if 'javascript' not in a['href']]
        except:
            sku_images = None

        for tr in positions_table:
            sku_article = None
            sku_barcode = None
            sku_weight_min = None
            sku_volume_min = None
            sku_quantity_min = None
            price_promo = None
            price = None
            sku_status = None

            td = tr.select('td')
            if not len(td):
                self.position_warning()
                break

            try:
                sku_article = td[0].select('b')[1].text
            except:
                prd_logger.warning(f'product sku_article not found in {self.sku_link}')
                pass

            try:
                sku_barcode = td[1].select('b')[1].text
            except:
                prd_logger.warning(f'product sku_barcode not found in {self.sku_link}')
                pass

            try:
                packing = td[2].select('b')[1].text
                if 'г' in packing:
                    sku_weight_min = packing
                if 'шт' in packing:
                    sku_quantity_min = packing
                if 'л' in packing:
                    sku_volume_min = packing
            except:
                prd_logger.warning(f'product packing not found in {self.sku_link}')
                pass

            try:
                price = td[4].select_one('s').get_text().split(' ')
                price = price[0]+price[1] if price[1].isdigit() else price[0]
            except:
                pass

            try:
                price_ = td[4].select_one('span').get_text().split(' ')
                price_ = price_[0] + price_[1] if price_[1].isdigit() else price_[0]
                if not price:
                    price = price_
                else:
                    price_promo = price_
            except:
                prd_logger.warning(f'product price/price_promo not found in {self.sku_link}')
                pass

            try:
                if tr.select_one('div.catalog-item-no-stock').get_text():
                    sku_status = 0
            except:
                sku_status = 1

            yield {
                'price_datetime': price_datetime,
                'price': price,
                'price_promo': price_promo,
                'sku_status': sku_status,
                'sku_barcode': sku_barcode,
                'sku_article': sku_article,
                'sku_name': sku_name,
                'sku_category': sku_category,
                'sku_country': sku_country,
                'sku_weight_min': sku_weight_min,
                'sku_volume_min': sku_volume_min,
                'sku_quantity_min': sku_quantity_min,
                'sku_link': self.sku_link,
                'sku_images': sku_images
            }

    def position_warning(self):
        prd_logger.warning(f'positions not found on page {self.sku_link}')

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val:
            raise
