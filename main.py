import logging
import re
from datetime import datetime, timezone, timedelta
from typing import List

from pydantic.type_adapter import TypeAdapter

from config import settings
from model import Destination, Message
from push.push_api import PushApi
from push.smtp.email_push import EmailPush
from weather.colorfulclouds.colorful_clouds_api import ColorfulCloudsApi
from weather.qweather.qweather_api import QWeatherApi
from weather.weather_api import WeatherApi

# Set log level
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y.%m.%d %H:%M:%S')

TZ_SHANGHAI = timezone(timedelta(hours=8), name='Asia/Shanghai')


def load_destinations() -> List[Destination]:
    with open('destinations.json', 'r', encoding='utf-8') as f:
        return TypeAdapter(List[Destination]).validate_json(f.read())


def get_weather_api() -> WeatherApi:
    logging.info(f'get weather api: {settings.provider.weather}')
    match settings.provider.weather:
        case 'colorful_clouds':
            return ColorfulCloudsApi()
        case 'qweather':
            return QWeatherApi()


def get_push_api() -> PushApi:
    logging.info(f'get weather api: {settings.provider.push}')
    match settings.provider.push:
        case 'smtp':
            return EmailPush()


def do_fetch_weather() -> Message | None:
    destinations = load_destinations()
    if not destinations:
        logging.info('Destinations is empty')
        return None

    weather_api = get_weather_api()
    if not weather_api:
        logging.error(f'Can not find weather api: {settings.provider.weather}')
        return None

    destination_weathers = weather_api.get_destination_future_weather(destinations)
    if not destination_weathers:
        logging.info(f'There is no good weather on those cities.')
        return None

    message = weather_api.parse_destination_weather(destination_weathers)
    if not message:
        logging.info(f'Parse destination weather failed. {destination_weathers}')
        return None

    push_api = get_push_api()
    if not push_api:
        logging.error(f'Can not find push api: {settings.provider.push}')
        return None

    if push_api.send_push(message):
        logging.info('Push message success.')
    else:
        logging.error(f'Push message failed: {settings.provider.push}')

    return message


def update_readme(new_content):
    logging.info('Update readme...')
    with open('README.md', 'r+', encoding='utf-8') as f:
        readme = f.read()
        pattern = re.compile(r'(?<=## Current Status).*?(?=## How to use)', re.DOTALL)
        new_content = re.sub(pattern, f'\n\n```\n{new_content}\n```\n\n', readme)
        f.seek(0)
        f.write(new_content)
        f.truncate()
    logging.info('Update readme success.')


if __name__ == '__main__':
    message = do_fetch_weather()
    today = datetime.now(TZ_SHANGHAI).strftime('%Y-%m-%d')
    content = f'{today} - '
    if message:
        content += '晴好假日提醒\n\n' + message.content
    else:
        content += f'未来暂无晴好假日'
    logging.info(content)
    update_readme(content)
