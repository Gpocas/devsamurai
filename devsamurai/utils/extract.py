from typing import List
from httpx import get
from parsel import Selector
from pprint import pprint

def get_html(url: str) -> str:
    response = get(url)
    return response.text


def get_links(html: str) -> List[str]:
    selector = Selector(text=html)

    links = selector.xpath('//li/a/@href').getall()

    valid_links = [link for link in links if link.endswith('zip')]
    return valid_links

if __name__ == '__main__':
    url = 'https://class.devsamurai.com.br/'
    html = get_html(url)
    links = get_links(html)
    pprint(links)


