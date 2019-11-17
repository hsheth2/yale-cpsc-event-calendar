import requests
from bs4 import BeautifulSoup


def parse_event_urls_from_feed(domain, feed):
    content = requests.get(feed)

    soup = BeautifulSoup(content.text, 'html5lib')
    soup.prettify()

    view = soup.body.find(class_='view-id-calendar_list')

    urls = []
    for link in view.find_all('a'):
        url = link.get('href')
        if url[0] == '/':
            url = f'{domain}{url}'
        urls.append(url)
    return urls
