from typing import List, Pattern
import requests
from bs4 import BeautifulSoup
import pytz
import datetime
import re

from common import Event

IGNORED_URL_PATTERNS: List[Pattern] = [
    re.compile(r"^https://yale.zoom.us/"),
]

REJECT_EVENT_URLS = {
    # site crashes with "site under maintenance"
    "https://frankeprogram.yale.edu/event/distinguished-speaker-series-talk-hazel-carby",
}


def parse_event_urls_from_feed(domain: str, feed: str) -> List[str]:
    content = requests.get(feed)

    soup = BeautifulSoup(content.text, "html5lib")
    soup.prettify()

    view = soup.body.find(class_="view-id-calendar_list")

    urls = []
    for link in view.select(".views-field-title a"):
        url = link.get("href")
        if url[0] == "/":
            url = f"{domain}{url}"
        if not any(pattern.match(url) for pattern in IGNORED_URL_PATTERNS):
            urls.append(url)
        else:
            print(f"skipping {url} - matches an ignore regex")
    return urls


def scrape_event_info(event_url: str) -> Event:
    page = requests.get(event_url)

    soup = BeautifulSoup(page.text, "html5lib")
    soup.prettify()

    content = soup.find(id="region-content")

    title_region = content.find(id="page-title")
    title = title_region.get_text().strip()

    # TODO: Capture start and end times.
    time_region = content.find(class_="field-name-field-event-time")
    time_element = time_region.find(class_="date-display-start")
    if not time_element:
        # Fallback to date-display-single if start is not available.
        time_element = time_region.find(class_="date-display-single")
    time_raw = time_element.get("content")
    time_aware = datetime.datetime.strptime(time_raw, "%Y-%m-%dT%H:%M:%S%z")
    time_real = time_aware.astimezone(tz=pytz.utc).replace(tzinfo=None)

    try:
        location_region = content.find(class_="field-name-field-location")
        location_region = location_region.find(class_="location")
        location_region.find("span", class_="map-icon").extract()
        location_name = location_region.find(class_="fn").get_text().strip()
    except:
        location_name = "TBA"

    description_region = content.find(class_="field-name-body")
    if description_region:
        description_texts = description_region.findAll(text=True)
        description = "\n".join(text.strip() for text in description_texts)
        # description = ''.join(description_texts)
    else:
        description = "No description provided"
    description += "\n\n" + event_url

    return Event(
        title=title,
        time=time_real,
        location=location_name,
        description=description,
        url=event_url,
    )


def fetch_upcoming_urls(domain: str, feeds: List[str]) -> List[str]:
    urls = []
    for feed in feeds:
        urls += parse_event_urls_from_feed(domain, feed)
    return urls


def fetch_upcoming_events(urls: List[str]) -> List[Event]:
    events = []
    for url in urls:
        print(f"starting {url}")
        if url in REJECT_EVENT_URLS:
            print("skipping because of rejection list")
            continue
        event_info = scrape_event_info(url)
        print(f"Event: {event_info.title}")
        events.append(event_info)

    return events
