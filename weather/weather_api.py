from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from typing import List

from model import Destination, DestinationWeather, Message


class WeatherApi(ABC):

    def get_destination_future_weather(self, destinations: List[Destination]) -> List[DestinationWeather]:
        with ThreadPoolExecutor(max_workers=10) as executor:
            destination_weather_futures = executor.map(self.get_destination_weather, destinations)
            return [destination_weather for destination_weather in destination_weather_futures if
                    destination_weather is not None]

    @abstractmethod
    def get_destination_weather(self, destination: Destination) -> DestinationWeather | None:
        pass

    def parse_destination_weather(self, destination_weathers: List[DestinationWeather]) -> Message:
        body = ''
        for destination_weather in destination_weathers:
            destination = destination_weather.destination
            weathers = destination_weather.weathers
            body += f'\n{destination.name} 更新时间 - {destination_weather.update_time.strftime("%Y-%m-%d %H:%M")}:\n'
            for weather in weathers:
                body += (f'{datetime.strftime(weather.date, "%Y-%m-%d")} 天气: {weather.day} '
                         f'云量：{weather.cloud} 最高气温: {weather.temp_max}°C 最低气温: {weather.temp_min}°C '
                         f'夜间：{weather.night}\n')
        return Message('以下城市将在假期内有晴好天气', body)
