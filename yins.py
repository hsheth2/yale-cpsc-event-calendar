from pprint import pprint

from scraping_common import fetch_upcoming_urls, fetch_upcoming_events
from generate_ics import generate_ics

domain = 'https://yins.yale.edu'
schedule_url = 'https://yins.yale.edu/calendar/speaker-schedule'
programs_url = 'https://yins.yale.edu/calendar/conferences-workshops'

def yins_generate(filename):
    print('Generating YINS Calendar')
    urls = fetch_upcoming_urls(domain, [schedule_url, programs_url])
    events = fetch_upcoming_events(urls)

    with open(filename, 'wb') as f:
        cal = generate_ics('YINS Events', 'Yale Institute for Network Sciences (YINS) Events Calendar', events)
        f.write(cal)
    print()


if __name__ == '__main__':
    urls = fetch_upcoming_urls(domain, [schedule_url, programs_url])
    pprint(urls)

    events = fetch_upcoming_events(urls)
    pprint(events)
