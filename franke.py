from pprint import pprint

from scraping_common import fetch_upcoming_urls, fetch_upcoming_events
from generate_ics import generate_ics

domain = 'https://frankeprogram.yale.edu'
upcoming_events_url = f'{domain}/calendar'


def franke_generate(filename):
    print('Generating Franke Program Calendar')
    urls = fetch_upcoming_urls(domain, [upcoming_events_url])
    events = fetch_upcoming_events(urls)

    with open(filename, 'wb') as f:
        cal = generate_ics('Yale Franke Program', 'Yale Franke Program in Science and the Humanities Event Calendar', events)
        f.write(cal)
    print()


if __name__ == '__main__':
    urls = fetch_upcoming_urls(domain, [upcoming_events_url])
    pprint(urls)

    events = fetch_upcoming_events(urls)
    pprint(events)
