from parsers import CatalogParser, CategoryParser
from helpers import CFG_helper, get_logger
import time

main_logger = get_logger(__name__)


def restarter(fn):
    def wrapper(*args, **kwargs):
        for _ in range(CFG_helper().get_restart()['restart_count']):
            try:
                return fn(*args, **kwargs)
            except:
                print('Critical error. Parser would be restarted.')
                main_logger.exception('exception')
                time.sleep(CFG_helper().get_restart()['interval_m']*60)
    return wrapper


@restarter
def parse_catalog():
    with CatalogParser(source) as cat_parser:
        return cat_parser.parse_catalog(subcatalog=CFG_helper().get_categories())


@restarter
def parse_categories(ctlg_href_list: list):
    with CategoryParser(source) as cat_parser:
        return cat_parser.parse_categories(ctlg_href_list)


if __name__ == '__main__':
    source = 'https://zootovary.ru/'

    ctlg_href_list = parse_catalog()

    if ctlg_href_list:
        parse_categories(ctlg_href_list)
