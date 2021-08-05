from typing import List
import requests
from bs4 import BeautifulSoup
import pytz
import datetime
import re

IGNORED_URL_PATTERNS: List[re.Pattern] = [
    re.compile(r'^https://yale.zoom.us/'),
]


def parse_event_urls_from_feed(domain: str, feed: str) -> List[str]:
    content = requests.get(feed)

    soup = BeautifulSoup(content.text, 'html5lib')
    soup.prettify()

    view = soup.body.find(class_='view-id-calendar_list')

    urls = []
    for link in view.select('.views-field-title a'):
        url = link.get('href')
        if url[0] == '/':
            url = f'{domain}{url}'
        if not any(pattern.match(url) for pattern in IGNORED_URL_PATTERNS):
            urls.append(url)
        else:
            print(f'skipping {url} - matches an ignore regex')
    return urls


def scrape_event_info(event_url: str):
    page = requests.get(event_url)

    soup = BeautifulSoup(page.text, 'html5lib')
    soup.prettify()

    content = soup.find(id='region-content')

    title_region = content.find(id='page-title')
    title = title_region.get_text().strip()

    # TODO: Capture start and end times.
    time_region = content.find(class_='field-name-field-event-time')
    time_element = time_region.find(class_='date-display-start')
    if not time_element:
        # Fallback to date-display-single if start is not available.
        time_element = time_region.find(class_='date-display-single')
    time_raw = time_element.get('content')
    time_aware = datetime.datetime.strptime(time_raw, "%Y-%m-%dT%H:%M:%S%z")
    time_real = time_aware.astimezone(tz=pytz.utc).replace(tzinfo=None)

    try:
        location_region = content.find(class_='field-name-field-location')
        location_region = location_region.find(class_='location')
        location_region.find('span', class_='map-icon').extract()
        location_name = location_region.find(class_='fn').get_text().strip()
    except:
        location_name = "TBA"

    description_region = content.find(class_='field-name-body')
    if description_region:
        description_texts = description_region.findAll(text=True)
        description = '\n'.join(text.strip() for text in description_texts)
        # description = ''.join(description_texts)
    else:
        description = 'No description provided'
    description += '\n\n' + event_url

    return {
        'title': title,
        'time': time_real,
        'location': location_name,
        'description': description,
        'url': event_url,
    }


def fetch_upcoming_urls(domain, feeds):
    urls = []
    for feed in feeds:
        urls += parse_event_urls_from_feed(domain, feed)
    return urls

def fetch_upcoming_events(urls):
    events = []
    for url in urls:
        print(f'starting {url}')
        event_info = scrape_event_info(url)
        print(f"Event: {event_info['title']}")
        events.append(event_info)

    return events
