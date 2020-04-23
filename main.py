import collections
from pprint import pprint

from scraping_common import fetch_upcoming_urls, fetch_upcoming_events
from generate_ics import generate_ics

DataSource = collections.namedtuple('DataSource',
    ['shortname', 'domain', 'feeds', 'title', 'description'])

cpsc = DataSource(
    shortname='CPSC',
    domain='https://cpsc.yale.edu',
    feeds = ['https://cpsc.yale.edu/calendar'],
    title='Yale CS Events',
    description='Yale Department of Computer Science',
)

franke = DataSource(
    shortname='Franke',
    domain='https://frankeprogram.yale.edu',
    feeds=['https://frankeprogram.yale.edu/calendar'],
    title='Yale Franke Program Events',
    description='Yale Franke Program in Science and the Humanities',
)

yins = DataSource(
    shortname='YINS',
    domain='https://yins.yale.edu',
    feeds=['https://yins.yale.edu/calendar/speaker-schedule',
        'https://yins.yale.edu/calendar/conferences-workshops'],
    title='YINS Events',
    description='Yale Institute for Network Sciences (YINS)',
)


def main(sources):
    for data in sources:
        print(f'Generating {data.shortname} Calendar')
        urls = fetch_upcoming_urls(data.domain, data.feeds)
        events = fetch_upcoming_events(urls)

        filename = f'calendars/{data.shortname.lower()}_events.ics'
        with open(filename, 'wb') as f:
            cal = generate_ics(data.title, data.description, events)
            f.write(cal)
        print()


if __name__ == '__main__':
    main([cpsc, franke, yins])

