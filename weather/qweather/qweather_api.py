import logging
from datetime import datetime

import requests
from chinese_calendar import is_holiday
from pydantic.type_adapter import TypeAdapter
from requests import HTTPError

from model import Destination, DestinationWeather, Weather
from weather.qweather.model import QWeather, Daily
from weather.weather_api import WeatherApi


def daily_to_weather(daily: Daily) -> Weather:
    return Weather(
        datetime.strptime(daily.fx_date, '%Y-%m-%d'),
        daily.text_day,
        daily.text_night,
        daily.temp_max,
        daily.temp_min,
        daily.cloud
    )


def check_weather_is_sunny(weather: Weather) -> bool:
    if not is_holiday(weather.date):
        return False
    return weather.day == '晴'


class QWeatherApi(WeatherApi):
    url: str
    api_key: str
    range: str
    session: requests.Session

    def __init__(self):
        from config import settings
        self.range = settings.qweather.range
        self.url = 'https://devapi.qweather.com/v7/weather/' + self.range
        self.api_key = settings.qweather.api_key
        self.session = requests.Session()

    def get_destination_weather(self, destination: Destination) -> DestinationWeather | None:
        logging.info(f'Requesting weather for {destination.name} for the next days')
        params = {'key': self.api_key, 'location': destination.location}
        try:
            response = self.session.get(url=self.url, params=params)
            response.raise_for_status()
            data = response.json()
            qweather = TypeAdapter(QWeather).validate_python(data)
            if qweather.code == '200':
                return self.handle_qweather(destination, qweather)
            else:
                logging.error(data)
        except HTTPError as ex:
            logging.error(f'HTTPError occurred while requesting weather for {destination.name}: {ex}')
        except requests.RequestException as ex:
            logging.error(f'RequestException occurred while requesting weather for {destination.name}: {ex}')
        except (ValueError, KeyError) as ex:
            logging.error(f'Error occurred while parsing weather data for {destination.name}: {ex}')
        except Exception as ex:
            logging.error(f'Error occurred while validate weather data for {destination.name}: {ex}')
        return None

    def handle_qweather(self, destination: Destination, qweather: QWeather) -> DestinationWeather | None:
        sunny_weather = []
        for daily in qweather.daily:
            weather = daily_to_weather(daily)
            if check_weather_is_sunny(weather):
                logging.info(f'{destination.name} has good weather on {datetime.strftime(weather.date, "%Y-%m-%d")}.')
                sunny_weather.append(weather)
        if sunny_weather:
            update_time = datetime.strptime(qweather.update_time, '%Y-%m-%dT%H:%M%z')
            return DestinationWeather(destination, update_time, sunny_weather)
        logging.info(f'{destination.name} has no good weather on {self.range}.')
        return None
