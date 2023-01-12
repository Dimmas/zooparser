#!/usr/bin/env python
#coding: utf-8

from parsers import CatalogParser, CategoryParser
from helpers import get_logger
from settings import config
import time

main_logger = get_logger(__name__)


def restarter(fn):
    def wrapper(*args, **kwargs):
        for _ in range(config.RESTART_COUNT):
            try:
                return fn(*args, **kwargs)
            except:
                print('Critical error. Parser would be restarted.')
                main_logger.exception('exception')
                time.sleep(config.RESTART_INTERVAL*60)
    return wrapper


@restarter
def parse_catalog():
    with CatalogParser(source) as cat_parser:
        return cat_parser.parse_catalog(subcatalog=config.CATEGORIES)


@restarter
def parse_categories(ctlg_href_set: set):
    with CategoryParser(source) as cat_parser:
        return cat_parser.parse_categories(ctlg_href_set)


if __name__ == '__main__':
    source = 'https://zootovary.ru/'

    ctlg_href_set = parse_catalog()

    if ctlg_href_set:
        parse_categories(ctlg_href_set)
