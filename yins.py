import datetime
from pprint import pprint
import pytz
import requests
from bs4 import BeautifulSoup

from scraping_common import parse_event_urls_from_feed
from generate_ics import generate_ics

domain = 'https://yins.yale.edu'
schedule_url = 'https://yins.yale.edu/calendar/speaker-schedule'
programs_url = 'https://yins.yale.edu/calendar/conferences-workshops'


def yins_get_events():
    schedule_urls = parse_event_urls_from_feed(domain, schedule_url)
    programs_urls = parse_event_urls_from_feed(domain, programs_url)

    return schedule_urls + programs_urls


def yins_event_info(event_url):
    page = requests.get(event_url)

    soup = BeautifulSoup(page.text, 'html5lib')
    soup.prettify()

    content = soup.find(id='region-content')

    title_region = content.find(id='page-title')
    title = title_region.get_text().strip()

    time_element = content.find('span', {'property': 'dc:date'})
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


def yins_generate(filename):
    with open(filename, 'wb') as f:
        print('Generating YINS Calendar')

        events = []
        urls = yins_get_events()
        for url in urls:
            event_info = yins_event_info(url)
            print(f"Event: {event_info['title']}")
            events.append(event_info)

        cal = generate_ics('YINS Events', 'Yale Institute for Network Sciences (YINS) Events Calendar', events)
        f.write(cal)
        print()


if __name__ == '__main__':
    results = yins_get_events()
    pprint(results)

    event_info = yins_event_info(results[0])
    pprint(event_info)
