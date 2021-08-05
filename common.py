import dataclasses
from datetime import datetime
from typing import List


@dataclasses.dataclass
class DataSource:
    shortname: str
    domain: str
    feeds: List[str]
    title: str
    description: str


@dataclasses.dataclass
class Event:
    title: str
    time: datetime
    location: str
    description: str
    url: str
