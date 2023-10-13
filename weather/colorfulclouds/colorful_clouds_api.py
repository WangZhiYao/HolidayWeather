import logging
from datetime import datetime, timezone, timedelta
from string import Template

import requests
from chinese_calendar import is_holiday
from pydantic.type_adapter import TypeAdapter
from requests import HTTPError

from model import Destination, DestinationWeather, Weather
from weather.colorfulclouds.model import ColorfulWeather
from weather.weather_api import WeatherApi

TZ_SHANGHAI = timezone(timedelta(hours=8), name='Asia/Shanghai')

skycon_map = {
    'CLEAR_DAY': '晴', 'CLEAR_NIGHT': '晴', 'PARTLY_CLOUDY_DAY': '多云', 'PARTLY_CLOUDY_NIGHT': '多云', 'CLOUDY': '阴',
    'LIGHT_HAZE': '轻度雾霾', 'MODERATE_HAZE': '中度雾霾', 'HEAVY_HAZE': '重度雾霾', 'LIGHT_RAIN': '小雨',
    'MODERATE_RAIN': '中雨', 'HEAVY_RAIN': '大雨', 'STORM_RAIN': '暴雨', 'FOG': '雾', 'LIGHT_SNOW': '小雪',
    'MODERATE_SNOW': '中雪', 'HEAVY_SNOW': '大雪', 'STORM_SNOW': '暴雪', 'DUST': '浮尘', 'SAND': '沙尘', 'WIND': '大风'
}


class ColorfulCloudsApi(WeatherApi):
    url: Template
    api_key: str
    range: str
    session: requests.Session

    def __init__(self):
        from config import settings
        self.url = Template('https://api.caiyunapp.com/v2.6/$api_key/$location/daily')
        self.api_key = settings.colorful_clouds.api_key
        self.range = settings.colorful_clouds.range
        self.session = requests.Session()

    def get_destination_weather(self, destination: Destination) -> DestinationWeather | None:
        logging.info(f'Requesting weather for {destination.name} for the next days')
        url = self.url.substitute(api_key=self.api_key, location=destination.location)
        params = {'dailysteps': self.range}
        try:
            response = self.session.get(url=url, params=params)
            response.raise_for_status()
            data = response.json()
            colorful_weather = TypeAdapter(ColorfulWeather).validate_python(data)
            if colorful_weather.status == 'ok' and colorful_weather.result.daily.status == 'ok':
                return self.handle_colorful_clouds(destination, colorful_weather)
            else:
                logging.error(colorful_weather)
        except HTTPError as ex:
            logging.error(f'HTTPError occurred while requesting weather for {destination.name}: {ex}')
        except requests.RequestException as ex:
            logging.error(f'RequestException occurred while requesting weather for {destination.name}: {ex}')
        except (ValueError, KeyError) as ex:
            logging.error(f'Error occurred while parsing weather data for {destination.name}: {ex}')
        except Exception as ex:
            logging.error(f'Error occurred while validate weather data for {destination.name}: {ex}')
        return None

    def handle_colorful_clouds(self, destination: Destination,
                               colorful_weather: ColorfulWeather) -> DestinationWeather | None:
        daily = colorful_weather.result.daily
        temperature_list = daily.temperature
        cloudrate_list = daily.cloudrate
        skycon_list = daily.skycon
        skycon_08h_20h_list = daily.skycon_08h_20h
        skycon_20h_32h_list = daily.skycon_20h_32h

        sunny_weather = []
        for index, skycon in enumerate(skycon_list):
            date = datetime.strptime(skycon.date, '%Y-%m-%dT%H:%M%z')
            if not is_holiday(date):
                continue
            if skycon_map[skycon.value] == '晴':
                sunny_weather.append(
                    Weather(
                        date,
                        skycon_map[skycon_08h_20h_list[index].value],
                        skycon_map[skycon_20h_32h_list[index].value],
                        str(temperature_list[index].max),
                        str(temperature_list[index].min),
                        str(cloudrate_list[index].avg)
                    )
                )
        if sunny_weather:
            return DestinationWeather(destination, datetime.now(TZ_SHANGHAI), sunny_weather)
        logging.info(f'{destination.name} has no good weather on next {self.range} days.')
        return None
