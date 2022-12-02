from parsers import CatalogParser, CategoryParser


if __name__ == '__main__':
    source = 'https://zootovary.ru/'
    subcatalog = [
        'tovary-i-korma-dlya-sobak/korm-sukhoy/belcando',
        'tovary-i-korma-dlya-koshek/korm-lechebnyy/hill-s'
    ]
    #subcatalog = None

    with CatalogParser(source) as cat_parser:
        ctlg_href_set = cat_parser.parse_catalog(subcatalog=subcatalog)

    with CategoryParser(source) as cat_parser:
        cat_parser.parse_category(ctlg_href_set)
