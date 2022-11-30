from helpers import CTLG_Helper, PG_Helper
from enums import Futures


def parse_ctlg(source):
    html = PG_Helper(source).get_text()
    ctlg_parser = CTLG_Helper(html, future=Futures.id_, future_name='catalog-menu')
    #ctlg_parser.get_catalog()
    ctlg_parser.get_catalog(node='/tovary-i-korma-dlya-koshek/')
    for _, child_href in ctlg_parser.get_childs():
        print(source+child_href[1:])
    ctlg_parser.save_catalog(ctlg_parser.get_childs_list())


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    parse_ctlg('https://zootovary.ru/')
