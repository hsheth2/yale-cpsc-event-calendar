import requests
from bs4 import BeautifulSoup

domain = 'https://cpsc.yale.edu'
upcoming_events_url = f'{domain}/calendar'

def get_upcoming_event_urls():
    content = requests.get(upcoming_events_url)

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


if __name__ == '__main__':
    results = get_upcoming_event_urls()
    print(results)

