from dataclasses import dataclass
from typing import List

from pydantic import BaseModel, Field


@dataclass
class Daily(BaseModel):
    fx_date: str = Field(alias='fxDate')
    temp_max: str = Field(alias='tempMax')
    temp_min: str = Field(alias='tempMin')
    text_day: str = Field(alias='textDay')
    text_night: str = Field(alias='textNight')
    cloud: str = Field(alias='cloud')


@dataclass
class QWeather(BaseModel):
    code: str
    daily: List[Daily]
    update_time: str = Field(alias='updateTime')
