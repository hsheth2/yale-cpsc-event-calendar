from pprint import pprint
import requests
from bs4 import BeautifulSoup

from scraping_common import parse_event_urls_from_feed, scrape_event_info
from generate_ics import generate_ics

domain = 'https://frankeprogram.yale.edu'
upcoming_events_url = f'{domain}/calendar'


def franke_upcoming_events():
    return parse_event_urls_from_feed(domain, upcoming_events_url)


def franke_generate(filename):
    with open(filename, 'wb') as f:
        print('Generating Franke Program Calendar')

        events = []
        urls = franke_upcoming_events()
        for url in urls:
            event_info = scrape_event_info(url)
            print(f"Event: {event_info['title']}")
            events.append(event_info)

        cal = generate_ics('Yale Franke Program', 'Yale Franke Program in Science and the Humanities Event Calendar', events)
        f.write(cal)
        print()


if __name__ == '__main__':
    results = franke_upcoming_events()
    pprint(results)

    event_info = scrape_event_info(results[0])
    pprint(event_info)
