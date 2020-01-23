from pprint import pprint
import requests
from bs4 import BeautifulSoup

from scraping_common import parse_event_urls_from_feed, scrape_event_info
from generate_ics import generate_ics

domain = 'https://yins.yale.edu'
schedule_url = 'https://yins.yale.edu/calendar/speaker-schedule'
programs_url = 'https://yins.yale.edu/calendar/conferences-workshops'


def yins_get_events():
    schedule_urls = parse_event_urls_from_feed(domain, schedule_url)
    programs_urls = parse_event_urls_from_feed(domain, programs_url)

    return schedule_urls + programs_urls


def yins_generate(filename):
    with open(filename, 'wb') as f:
        print('Generating YINS Calendar')

        events = []
        urls = yins_get_events()
        for url in urls:
            event_info = scrape_event_info(url)
            print(f"Event: {event_info['title']}")
            events.append(event_info)

        cal = generate_ics('YINS Events', 'Yale Institute for Network Sciences (YINS) Events Calendar', events)
        f.write(cal)
        print()


if __name__ == '__main__':
    results = yins_get_events()
    pprint(results)

    event_info = scrape_event_info(results[0])
    pprint(event_info)
