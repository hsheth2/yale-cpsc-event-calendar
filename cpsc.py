import datetime
from pprint import pprint
import pytz
import requests
from bs4 import BeautifulSoup

from generate_ics import generate_ics

domain = 'https://cpsc.yale.edu'
upcoming_events_url = f'{domain}/calendar'


def cpsc_upcoming_events():
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


def cpsc_event_info(event_url):
    page = requests.get(event_url)

    soup = BeautifulSoup(page.text, 'html5lib')
    soup.prettify()

    content_region = soup.find(id='region-content')

    title_region = content_region.find(id='page-title')
    title = title_region.get_text().strip()

    content = content_region.find('article', class_='node-event')
    content = content.find(class_='content')

    time_region = content.find(class_='field-name-field-event-time')
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
    description_texts = description_region.findAll(text=True)
    description = '\n'.join(text.strip() for text in description_texts)
    # description = ''.join(description_texts)

    return {
        'title': title,
        'time': time_real,
        'location': location_name,
        'description': description,
        'url': event_url,
    }


def cpsc_events():
    events = []
    urls = cpsc_upcoming_events()
    for url in urls:
        event_info = cpsc_event_info(url)
        print(f"Event: {event_info['title']}")
        events.append(event_info)

    return events


def cpsc_generate(filename):
    with open(filename, 'wb') as f:
        print('Generating CPSC Calendar')
        events = cpsc_events()
        cal = generate_ics('Yale CS Events', 'Yale CPSC Events Calendar', events)
        f.write(cal)
        print()


if __name__ == '__main__':
    results = cpsc_upcoming_events()
    pprint(results)

    event_info = cpsc_event_info(results[0])
    pprint(event_info)
