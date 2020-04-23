from pprint import pprint

from scraping_common import fetch_upcoming_urls, fetch_upcoming_events
from generate_ics import generate_ics

domain = 'https://cpsc.yale.edu'
upcoming_events_url = f'{domain}/calendar'


def cpsc_generate(filename):
    print('Generating CPSC Calendar')
    urls = fetch_upcoming_urls(domain, [upcoming_events_url])
    events = fetch_upcoming_events(urls)

    with open(filename, 'wb') as f:
        cal = generate_ics('Yale CS Events', 'Yale CPSC Events Calendar', events)
        f.write(cal)
    print()


if __name__ == '__main__':
    urls = fetch_upcoming_urls(domain, [upcoming_events_url])
    pprint(urls)

    events = fetch_upcoming_events(urls)
    pprint(events)
