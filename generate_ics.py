import datetime
import icalendar
import sys

from upcoming_urls import get_upcoming_event_urls
from event_information import get_event_information

def get_events():
    events = []
    urls = get_upcoming_event_urls()
    for url in urls:
        event_info = get_event_information(url)
        events.append(event_info)

    return events


def generate_ics(events):
    calendar = icalendar.Calendar()
    calendar.add('X-WR-CALNAME', 'Yale CS Events')
    calendar.add('X-WR-CALDESC', 'Yale CPSC Event Calendar')
    for event in events:
        cal_event = ics_event_from_event(event)
        calendar.add_component(cal_event)
    return calendar.to_ical()

def ics_event_from_event(event):
    cal = icalendar.Event()

    cal.add('SUMMARY', event['title'])
    cal.add('DESCRIPTION', event['description'])
    cal.add('URL', event['url'])
    cal.add('LOCATION', event['location'])
    cal.add('STATUS', 'CONFIRMED')

    cal.add('DTSTART', event['time'])
    cal.add('DTEND', event['time'] + datetime.timedelta(hours = 1))

    return cal


if __name__ == '__main__':
    events = get_events()
    cal = generate_ics(events)
    sys.stdout.buffer.write(cal)
