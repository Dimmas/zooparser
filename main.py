from helpers import CTLG_Helper, PG_Helper


def parse_ctlg(source):
    html = PG_Helper(source).get_text()
    ctlg_parser = CTLG_Helper(html, selector='#catalog-menu ul li.lev1')
    ctlg_parser.get_catalog()
    #ctlg_parser.get_catalog(node='/tovary-i-korma-dlya-koshek/')
    full_catalog = []
    for _, child_href in ctlg_parser.get_childs():
        html = PG_Helper(source+child_href[1:]).get_text()
        subctlg_parser = CTLG_Helper(html, selector='div.catalog-menu-left ul li')
        subctlg_parser.get_catalog()
        full_catalog += subctlg_parser.get_childs_list()
    ctlg_parser.save_catalog(full_catalog)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    parse_ctlg('https://zootovary.ru/')
