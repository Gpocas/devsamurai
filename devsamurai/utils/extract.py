import csv
from typing import List, Tuple
from httpx import get
from parsel import Selector
from unidecode import unidecode

def get_html(url: str) -> str:
    response = get(url)
    return response.text


def get_links(html: str) -> List[Tuple[str, str]]:
    selector = Selector(text=html)

    links = selector.css('li>a')
    data_links = []

    for link in links:
        link_href = link.attrib['href']
        
        if not link_href.endswith('zip'):
            continue
        
        link_text = link.xpath('text()').get()
        link_text = (
            unidecode(
                link_text
                .strip()
                .lower()
                .replace(' ', '_')
                .replace('-', '_')
                .replace('___', '_')
                .replace('__', '_')
            )
        )
        
        data = (link_text, link_href)
        data_links.append(data)
    
    return data_links


def save_links(links: List[Tuple[str, str]], filename: str) -> None:
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['name', 'url'])
        writer.writerows(links)

if __name__ == '__main__':
    url = 'https://class.devsamurai.com.br/'
    html = get_html(url)
    links = get_links(html)
    save_links(links, 'aulas.csv')


