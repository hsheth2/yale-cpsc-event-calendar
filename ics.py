import datetime
from typing import List
import icalendar
from common import Event


def generate_ics(title: str, desc: str, events: List[Event]) -> bytes:
    calendar = icalendar.Calendar()
    calendar.add('X-WR-CALNAME', title)
    calendar.add('X-WR-CALDESC', desc)
    for event in events:
        cal_event = ics_event_from_event(event)
        calendar.add_component(cal_event)
    return calendar.to_ical()


def ics_event_from_event(event: Event) -> icalendar.Event:
    cal = icalendar.Event()

    cal.add('SUMMARY', event.title)
    cal.add('DESCRIPTION', event.description)
    cal.add('URL', event.url)
    cal.add('LOCATION', event.location)
    cal.add('STATUS', 'CONFIRMED')

    cal.add('DTSTART', event.time)
    cal.add('DTEND', event.time + datetime.timedelta(hours=1))

    return cal


if __name__ == '__main__':
    event = Event(description= 'Event description:\n'
                            'Poynter Fellowship in Journalism\n'
                            'Ashlyn Still, Graphics Reporter\n'
                            'Washington Post\n'
                            '\n'
                            'Holly Rushmeier\n'
                            'is hosting Ashlyn Still\n'
                            '\n'
                            'News Graphics and Data Visualization\n'
                            '\n'
                            'The media landscape is changing rapidly and the tools used '
                            'for reporting and storytelling are changing with it. New '
                            'technologies have made data analysis and visualization more '
                            'accessible for reporters to tell stories in new and different '
                            'ways. The graphics team at The Washington Post is no '
                            'exception – they produce award-winning visual storytelling '
                            'using data, design, code, cartography, illustration, '
                            'animation, augmented reality and more. We’ll take a look at '
                            'how graphics reporters at The Post are using all of these '
                            'methods to enhance their storytelling and better reach '
                            'audiences in both the print and digital space.\n'
                            '\n',
             location= 'Franke Family Digital Humanities Laboratory in the Sterling '
                         'Memorial Library',
             time= datetime.datetime(2019, 11, 18, 21, 0),
             title= 'Poynter Fellowship in Journalism - Ashlyn Still, Graphics '
                      'Reporter/Washington Post',
             url= 'https://cpsc.yale.edu/event/poynter-fellowship-journalism-ashlyn-still-graphics-reporterwashington-post')

    with open('calendars/test.ics', 'wb') as f:
        data = generate_ics('Test Calendar', 'Test Calendar Desc', [event])
        f.write(data)
