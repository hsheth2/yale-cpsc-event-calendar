from pprint import pprint
import requests
from bs4 import BeautifulSoup

from scraping_common import parse_event_urls_from_feed, scrape_event_info
from generate_ics import generate_ics

domain = 'https://cpsc.yale.edu'
upcoming_events_url = f'{domain}/calendar'


def cpsc_upcoming_events():
    return parse_event_urls_from_feed(domain, upcoming_events_url)


def cpsc_generate(filename):
    with open(filename, 'wb') as f:
        print('Generating CPSC Calendar')

        events = []
        urls = cpsc_upcoming_events()
        for url in urls:
            event_info = scrape_event_info(url)
            print(f"Event: {event_info['title']}")
            events.append(event_info)

        cal = generate_ics('Yale CS Events', 'Yale CPSC Events Calendar', events)
        f.write(cal)
        print()


if __name__ == '__main__':
    results = cpsc_upcoming_events()
    pprint(results)

    event_info = scrape_event_info(results[0])
    pprint(event_info)
