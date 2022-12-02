from parsers import CatalogParser, CategoryParser
from helpers import CFG_helper
import time


def restarter(fn):
    def wrapper(*args, **kwargs):
        for _ in range(CFG_helper().get_restart()['restart_count']):
            try:
                return fn(*args, **kwargs)
            except:
                print('Critical error. Restart parsing.')
                time.sleep(CFG_helper().get_restart()['interval_m']*60)
    return wrapper


@restarter
def parse_catalog():
    with CatalogParser(source) as cat_parser:
        return cat_parser.parse_catalog(subcatalog=CFG_helper().get_categories())


@restarter
def parse_categories(ctlg_href_set: set):
    with CategoryParser(source) as cat_parser:
        return cat_parser.parse_categories(ctlg_href_set)


if __name__ == '__main__':
    source = 'https://zootovary.ru/'

    ctlg_href_set = parse_catalog()

    if ctlg_href_set:
        parse_categories(ctlg_href_set)

