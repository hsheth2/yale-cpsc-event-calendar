import requests
from bs4 import BeautifulSoup

def get_event_information(event_url):
    page = requests.get(event_url)

    soup = BeautifulSoup(page.text, 'html5lib')
    soup.prettify()

    content_region = soup.find(id='region-content')

    title_region = content_region.find(id='page-title')
    title = title_region.get_text().strip()

    content = content_region.find('article', class_='node-event')
    content = content.find(class_='content')

    time_region = content.find(class_='field-name-field-event-time')
    time_element = time_region.find(class_='date-display-single')
    time_raw = time_element.get('content')
    # TODO parse the time

    location_region = content.find(class_='field-name-field-location')
    location_region = location_region.find(class_='location')
    location_region.find('span', class_='map-icon').extract()
    location_name = location_region.find(class_='fn').get_text().strip()
    # TODO: Is it worthwhile getting the street address?

    description_region = content.find(class_='field-name-body')
    description_texts = description_region.findAll(text=True)
    description = '\n'.join(text.strip() for text in description_texts)
    #description = ''.join(description_texts)

    return {
        'title': title,
        'time': time_raw,
        'location': location_name,
        'description': description,
    }


if __name__ == '__main__':
    url = 'https://cpsc.yale.edu/event/cs-talk-yuhao-zhu-university-rochester'
    event_info = get_event_information(url)
    print(event_info)
