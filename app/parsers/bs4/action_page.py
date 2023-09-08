from bs4 import BeautifulSoup


class ActionPageParser(BeautifulSoup):

    def __init__(self, content: str | bytes, parser: str = 'html.parser'):
        super().__init__(content, parser)

    def parse_photo_links(self):
        for link_obj in self.select(
            '.swiper-wrapper .swiper-slide .swiper-zoom-container img'
        ):
            link1 = link_obj.get('src')
            link2 = link_obj.get('data-src')
            yield link1 if link1 else link2
