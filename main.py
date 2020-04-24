import collections
from pprint import pprint
import jinja2
import datetime
import pathlib
import shutil

from scraping_common import fetch_upcoming_urls, fetch_upcoming_events
from ics import generate_ics

DOMAIN_ROOT = 'https://yale-calendars.sheth.io'

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
    out_dir = 'gen'
    pathlib.Path(out_dir).mkdir(exist_ok=True)
    shutil.copyfile('templates/favicon.ico', f'{out_dir}/favicon.ico')

    # Generate calendars.
    for data in sources:
        print(f'Generating {data.shortname} Calendar')
        urls = fetch_upcoming_urls(data.domain, data.feeds)
        events = fetch_upcoming_events(urls)

        filename = f'{out_dir}/{data.shortname.lower()}_events.ics'
        with open(filename, 'wb') as f:
            cal = generate_ics(data.title, data.description, events)
            f.write(cal)
        print()

    # Generate index page.
    loader = jinja2.FileSystemLoader('./templates')
    env = jinja2.Environment(
        loader=loader,
        autoescape=jinja2.select_autoescape(['html', 'xml'])
    )
    template = env.get_template('index.html')
    index = template.render(
        domain_root=DOMAIN_ROOT,
        sources=sources,
        last_updated=datetime.datetime.now(datetime.timezone.utc).isoformat())
    with open(f'{out_dir}/index.html', 'w') as index_file:
        index_file.write(index)


if __name__ == '__main__':
    main([cpsc, franke, yins])

