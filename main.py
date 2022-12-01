from helpers import (
    CTLG_Helper,
    CTGR_Helper,
    PRD_Helper,
    PG_Helper
)


def parse_catalog(source):
    html = PG_Helper(source).get_text()
    ctlg_parser = CTLG_Helper(html, selector='#catalog-menu ul li.lev1')
    # ctlg_parser.get_catalog()
    ctlg_parser.get_catalog(node='/tovary-i-korma-dlya-khorkov/')
    full_catalog = []
    ctlg_href_set = set()
    for _, child_href in ctlg_parser.get_childs():
        html = PG_Helper(source + child_href[1:]).get_text()
        subctlg_parser = CTLG_Helper(html, selector='div.catalog-menu-left ul li')
        subctlg_parser.get_catalog()
        full_catalog += subctlg_parser.get_childs_list()
        ctlg_href_set = ctlg_href_set.union(subctlg_parser.get_href_set())
    ctlg_parser.save_csv(full_catalog)
    return ctlg_href_set


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
                print(page_num)
                cat_href_set_prod = cat_href_set_prod.union(parse_cat_page(href, page_num))
        print(len(cat_href_set_prod))


def parse_prod(href):
    html = PG_Helper(href).get_text()
    product_helper = PRD_Helper(html)
    print(product_helper.get_prod(selector='div.catalog-element-top'))


def parse_cat_page(href, page_num=1):
    html = PG_Helper(href + '&PAGEN_1=' + str(page_num)).get_text()
    cat_parser = CTGR_Helper(html)
    cat_parser.get_href_set_prod(selector='div.catalog-section a.name')
    return cat_parser.get_href_set()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    source = 'https://zootovary.ru/'
    """print('starting directory parsing')
    ctlg_href_set = parse_catalog(source)
    print('catalog parsing is completed')

    print('starting category parsing')
    parse_category(source, ctlg_href_set)"""


    prod_dict = parse_prod('https://zootovary.ru/catalog/tovary-i-korma-dlya-sobak/korm-sukhoy/nasha_marka_korm_dlya_sobak_srednikh_porod_myasom_tsyplenka_i_ovoshchami.html')
    print(prod_dict)
