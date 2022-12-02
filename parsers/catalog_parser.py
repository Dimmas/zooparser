from helpers import CTLG_Helper, PG_Helper


class CatalogParser:
    full_catalog = []

    def __init__(self, source: str):
        print('***')
        print('starting directory parsing')
        self.source = source

    def __enter__(self):
        return self

    def parse_catalog(self, subcatalog: list = None):
        ctlg_href_set = set()

        if subcatalog:
            for subcat in subcatalog:
                parent_catalog, *_, child_catalog = subcat.split('/')
                try:
                    full_cat, href_set = self.parse_subcatalog(
                        source=f'{self.source}catalog/{parent_catalog}/',
                        subcatalog=child_catalog
                    )
                    self.full_catalog += full_cat
                    ctlg_href_set = ctlg_href_set.union(href_set)
                except Exception as e:
                    print(e)
        else:
            html = PG_Helper(self.source).get_text()
            if not html:
                raise Exception('not connection to ', self.source)
            ctlg_parser = CTLG_Helper(html, selector='#catalog-menu ul li.lev1')
            ctlg_parser.get_catalog()
            for _, child_href in ctlg_parser.get_childs():
                try:
                    full_cat, href_set = self.parse_subcatalog(self.source + child_href[1:])
                    self.full_catalog += full_cat
                    ctlg_href_set = ctlg_href_set.union(href_set)
                except Exception as e:
                    print(e)
        return ctlg_href_set

    @staticmethod
    def parse_subcatalog(source, subcatalog=None):
        html = PG_Helper(source).get_text()
        if not html:
            raise Exception('not connection to ', source)
        subctlg_parser = CTLG_Helper(html, selector='div.catalog-menu-left ul li')
        subctlg_parser.get_catalog(subcatalog=subcatalog)
        return subctlg_parser.get_childs_list(), subctlg_parser.get_href_set()

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('catalog parsing is completed')
        if len(self.full_catalog):
            CTLG_Helper.save_csv(self.full_catalog)
        if exc_val:
            raise
