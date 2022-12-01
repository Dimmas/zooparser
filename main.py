from helpers import (
    CTLG_Helper,
    CTGR_Helper,
    PRD_Helper,
    PG_Helper
)


def parse_catalog(source: str, subcatalog:list =None):
    full_catalog = []
    ctlg_href_set = set()

    if subcatalog:
        for subcat in subcatalog:
            parent_catalog, *_, child_catalog = subcat.split('/')
            full_cat, href_set = parse_subcatalog(
                source=f'{source}catalog/{parent_catalog}/',
                subcatalog=child_catalog
            )
            full_catalog += full_cat
            ctlg_href_set = ctlg_href_set.union(href_set)
    else:
        html = PG_Helper(source).get_text()
        ctlg_parser = CTLG_Helper(html, selector='#catalog-menu ul li.lev1')
        ctlg_parser.get_catalog()
        for _, child_href in ctlg_parser.get_childs():
            full_cat, href_set = parse_subcatalog(source + child_href[1:])
            full_catalog += full_cat
            ctlg_href_set = ctlg_href_set.union(href_set)
    CTLG_Helper.save_csv(full_catalog)
    return ctlg_href_set


def parse_subcatalog(source:str, subcatalog=None):
    html = PG_Helper(source).get_text()
    subctlg_parser = CTLG_Helper(html, selector='div.catalog-menu-left ul li')
    subctlg_parser.get_catalog(subcatalog=subcatalog)
    return subctlg_parser.get_childs_list(), subctlg_parser.get_href_set()


def parse_category(source: str, href_set: set):
    cat_href_set_prod = set()
    for href in href_set:
        href = source[:-1] + href + '?pc=60'
        html = PG_Helper(href).get_text()
        cat_parser = CTGR_Helper(html)
        cat_page_count = int(cat_parser.get_page_count(selector='div.navigation a'))
        cat_href_set_prod = cat_href_set_prod.union(parse_cat_page(href))
        if cat_page_count:
            for page_num in range(2, cat_page_count + 1):
                cat_href_set_prod = cat_href_set_prod.union(parse_cat_page(href, page_num))
        print(len(cat_href_set_prod))


def parse_cat_page(href, page_num=1):
    html = PG_Helper(href + '&PAGEN_1=' + str(page_num)).get_text()
    cat_parser = CTGR_Helper(html)
    cat_parser.get_href_set_prod(selector='div.catalog-section a.name')
    if not cat_parser.get_href_set():
        print('category is empty: ', href)
    return cat_parser.get_href_set()


def parse_prod(href):
    html = PG_Helper(href).get_text()
    product_helper = PRD_Helper(html)
    product_helper.sku_link = href
    for product in product_helper.get_prod(selector='div.catalog-element-top'):
        print(product)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    source = 'https://zootovary.ru/'
    subcatalog = [
        'tovary-i-korma-dlya-sobak/korm-sukhoy/belcando',
        'tovary-i-korma-dlya-koshek/korm-lechebnyy/hill-s'
    ]
    #subcatalog = None

    print('starting directory parsing')
    ctlg_href_set = parse_catalog(source=source, subcatalog=subcatalog)
    print('catalog parsing is completed')

    print('starting category parsing')
    parse_category(source, ctlg_href_set)


    # parse_prod('https://zootovary.ru/catalog/tovary-i-korma-dlya-koshek/korm-sukhoy/1st-choice/1st_choice_kitten_healthy_start_korm_dlya_kotyat_zdorovyy_start.html')

