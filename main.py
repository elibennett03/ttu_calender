import requests
import xml.etree.ElementTree as ET
import json

# URL of the RSS feed
url = "https://api.calendar.moderncampus.net/pubcalendar/f108e9c9-1871-4e88-86ed-db960e023f12/rss?category=06384fe1-aeff-4550-a991-8ca25206afcb&category=2e83a8dc-fd56-4370-b039-50fea42747d4&category=c6fb44df-d59b-46d3-99af-d2aa5d93ac46&category=d5435357-2522-4aac-9460-bc9a70a2bc42&category=566e4391-cbb9-49ed-8e2a-bbc5474dd5b5&category=41a13092-6c97-453f-a372-152a4f7c6783&category=58db8015-4110-4d09-b130-d4233bcee784&category=766f55f6-318d-462a-a98a-a792d31b092b&category=24616d68-b423-4dd5-a52f-ced54a4b7c18&category=cf7d816a-c9ed-4800-9abd-9bff1cc83893&category=cd630417-0ef1-43ed-8714-979f4ed2da6a&category=017bc587-ecc0-4a99-abba-17c56baded7e&category=0c0f1095-8c5a-4060-acf7-8d8801efd491&category=545623e1-e1d6-4508-a55c-9fc7dacad4d2&category=2ff1ede5-ac4b-4470-89c8-998ee7baa9c6&category=7e1ad9e8-bf7e-4dd3-b06c-f1400b00294b&category=1dfe43be-80a6-4707-a35c-e071767de5df&category=10a7df06-e154-46e7-b23e-e608ee28e396&url=https%3A%2F%2Fwww.tntech.edu%2Fcalendar%2F"

# Fetch the RSS feed
response = requests.get(url)
response.raise_for_status()

# Parse the RSS feed
root = ET.fromstring(response.content)

# Extract event data
events = []
namespace = {
    'dc': 'http://purl.org/dc/elements/1.1/',
    'atom': 'http://www.w3.org/2005/Atom',
    'cal': 'https://moderncampus.com/Data/cal/'
}

def get_text_or_empty(element, tag, namespace):
    found_element = element.find(tag, namespace)
    return found_element.text if found_element is not None else ""

for item in root.findall("./channel/item"):
    event = {
        "title": get_text_or_empty(item, "title", namespace),
        "link": get_text_or_empty(item, "link", namespace),
        "pubDate": get_text_or_empty(item, "pubDate", namespace),
        "calendar": get_text_or_empty(item, "cal:calendar", namespace),
        "guid": get_text_or_empty(item, "cal:guid", namespace),
        "start": get_text_or_empty(item, "cal:start", namespace),
        "end": get_text_or_empty(item, "cal:end", namespace),
        "recurring": get_text_or_empty(item, "cal:recurring", namespace),
        "featured": get_text_or_empty(item, "cal:featured", namespace),
        "status": get_text_or_empty(item, "cal:status", namespace),
        "organizer": get_text_or_empty(item, "cal:organizer", namespace),
        "location": get_text_or_empty(item, "cal:location", namespace),
        "locationRoom": get_text_or_empty(item, "cal:locationRoom", namespace),
        "image": get_text_or_empty(item, "cal:image", namespace),
        "imageAltText": get_text_or_empty(item, "cal:imageAltText", namespace),
        "tags": [tag.text for tag in item.findall("cal:tags/cal:tag", namespace)]
    }
    events.append(event)

# Save the events to a JSON file
with open("events.json", "w") as f:
    json.dump(events, f, indent=4)

print("Events data saved to events.json")
