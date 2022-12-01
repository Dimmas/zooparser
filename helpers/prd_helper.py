from bs4 import BeautifulSoup


class PRD_Helper:

    def __init__(
            self,
            html
    ):
        self.bs4 = BeautifulSoup(html, "html.parser")

    def get_prod(self, selector):
        prod = self.bs4.select(selector)
        return prod
