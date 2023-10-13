from dataclasses import dataclass
from typing import List


@dataclass
class Temperature:
    date: str
    max: float
    min: float
    avg: float


@dataclass
class CloudRate:
    date: str
    max: float
    min: float
    avg: float


@dataclass
class SkyCon:
    date: str
    value: str


@dataclass
class Daily:
    status: str
    temperature: List[Temperature]
    temperature_08h_20h: List[Temperature]
    temperature_20h_32h: List[Temperature]
    cloudrate: List[CloudRate]
    skycon: List[SkyCon]
    skycon_08h_20h: List[SkyCon]
    skycon_20h_32h: List[SkyCon]


@dataclass
class Result:
    daily: Daily


@dataclass
class ColorfulWeather:
    status: str
    api_version: str
    api_status: str
    location: List[float]
    result: Result
