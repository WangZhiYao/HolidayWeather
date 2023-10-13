from dataclasses import dataclass
from datetime import datetime
from typing import List

from pydantic import BaseModel


@dataclass
class Destination(BaseModel):
    name: str
    location: str


@dataclass
class Weather:
    date: datetime
    day: str
    night: str
    temp_max: str
    temp_min: str
    cloud: str


@dataclass
class DestinationWeather:
    destination: Destination
    update_time: datetime
    weathers: List[Weather]


@dataclass
class Message:
    title: str
    content: str
