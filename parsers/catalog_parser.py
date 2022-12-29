from helpers import CTLG_Helper, PG_Helper, get_logger

catalog_logger = get_logger(__name__)


class CatalogParser:
    full_catalog = []

    def __init__(self, source: str):
        catalog_logger.info('*** starting catalog parsing ***')
        self.source = source

    def __enter__(self):
        return self

    def parse_catalog(self, subcatalog: list = None):

        if subcatalog:
            for subcat in subcatalog:
                parent_catalog, *_, child_catalog = subcat.split('/')
                try:
                    full_cat = self.parse_subcatalog(
                        source=f'{self.source}catalog/{parent_catalog}/',
                        subcatalog=child_catalog
                    )
                    self.full_catalog += full_cat
                except Exception as e:
                    catalog_logger.error(e)
        else:
            with PG_Helper(self.source) as pgh:
                html = pgh.get_text()
            if not html:
                raise Exception('not connection to ', self.source)
            with CTLG_Helper(html, selector='#catalog-menu ul li.lev1') as ctlg_parser:
                ctlg_parser.get_catalog()
                for _, child_href in ctlg_parser.get_childs():
                    try:
                        full_cat = self.parse_subcatalog(self.source + child_href[1:])
                        self.full_catalog += full_cat
                    except Exception as e:
                        catalog_logger.error(e)
        return self._get_href_set()

    def _get_href_set(self):
        if len(self.full_catalog):
            parents_set = {cat['parent_id'] for cat in self.full_catalog}
            return {cat['href'] for cat in self.full_catalog if cat['id'] not in parents_set}
        return set()

    @staticmethod
    def parse_subcatalog(source, subcatalog=None):
        with PG_Helper(source) as pgh:
            html = pgh.get_text()
        if not html:
            raise Exception(f'not connection to {source}')
        with CTLG_Helper(html, selector='div.catalog-menu-left ul li') as subctlg_parser:
            subctlg_parser.get_catalog(subcatalog=subcatalog)
            return subctlg_parser.get_childs_list()

    def __exit__(self, exc_type, exc_val, exc_tb):
        catalog_logger.info('*** catalog parsing is completed ***')
        if len(self.full_catalog):
            CTLG_Helper.save_csv(self.full_catalog)
        if exc_val:
            raise
