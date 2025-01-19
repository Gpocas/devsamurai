import csv
from typing import List, Tuple
from httpx import get
from parsel import Selector
from unidecode import unidecode
from devsamurai.utils.settings import Settings

s = Settings()

class ExtractDataWebSite:
    def __init__(self):
        self.url = 'https://class.devsamurai.com.br/'

    def get_html(self) -> str:
        response = get(self.url)
        return response.text

    def get_links(self, html: str) -> List[Tuple[str, str]]:
        selector = Selector(text=html)

        links = selector.css('li>a')
        data_links = []

        for link in links:
            link_href = link.attrib['href']

            if not link_href.endswith('zip'):
                continue

            link_text = link.xpath('text()').get()
            link_text = unidecode(
                link_text.strip()
                .lower()
                .replace(' ', '_')
                .replace('-', '_')
                .replace('___', '_')
                .replace('__', '_')
            )

            data = (link_text, link_href)
            data_links.append(data)

        return data_links

    def save_links(self, links: List[Tuple[str, str]]) -> None:
        with open(s.CSV_PATH, 'w', newline='') as file:
            writer = csv.writer(
                file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL
            )
            writer.writerow(['name', 'url', 'status'])
            writer.writerows(links)

    def genereate_csv(self) -> None:
        html = self.get_html()
        links = self.get_links(html)
        self.save_links(links)
