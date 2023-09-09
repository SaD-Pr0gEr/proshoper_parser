from bs4 import BeautifulSoup, ResultSet, Tag

from app.parsers.interfaces.catalog import CatalogData
from app.utils.date import DateFormatter


class CatalogParser(BeautifulSoup):

    def __init__(self, content: str | bytes, parser: str = 'html.parser'):
        super().__init__(content, parser)

    def parse_catalogs_block(self) -> ResultSet[Tag]:
        return self.select('.catalogs .catalog')

    def clean_text(self, text) -> str:
        symbols = ['<<', '>>', '"', "'", '»', '«']
        for symbol in symbols:
            text = text.replace(symbol, '')
        return text

    def parse_company_name(self) -> str:
        txt = self.find('span', class_='breadcrumbs-last').text
        return self.clean_text(txt)

    def parse_catalog_data(self, catalog_soup: Tag) -> CatalogData:
        link = catalog_soup.find('a', class_='catalog__link')['href']
        description_container = catalog_soup.find(class_='catalog__descr')
        catalog_divs = description_container.select('div')
        action_name = catalog_divs[0].find('b').text
        action_name = self.clean_text(action_name)
        action_dates = catalog_divs[1].text
        pages_count = int(
            catalog_soup.find('span', class_='catalog__counter')
            .text.split()[0]
        )
        split_link = link.split('/')
        if not split_link[-1].isdecimal():
            action_id = int(split_link[-2])
        else:
            action_id = int(split_link[-1])
        formatter = DateFormatter(action_dates)
        date_from, date_to = formatter.native_dates
        return CatalogData(
            action_name, date_from,
            date_to, pages_count, action_id, link
        )
