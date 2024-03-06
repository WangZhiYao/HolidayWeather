# Holiday Weather

This project utilizes Github Actions to schedule an automatic execution on workdays and retrieves weather data for the destination within the next couple of days by the  specified api.
This program checks if the weather is sunny on at least one day during the holiday. In such a case, it will send notification messages through the specified method.

Please note that the free version of the API only provides weather forecasts for 1-15 days, which means that this project is only suitable for impromptu weekend getaways.

## Current Status

```
2024-03-06 - 晴好假日提醒


泰山 更新时间 - 2024-03-06 08:36
2024-03-09 天气: 晴 云量：0.08 最高气温: 11.27°C 最低气温: -2.01°C 夜间：多云

威海 更新时间 - 2024-03-06 08:36
2024-03-09 天气: 晴 云量：0.0 最高气温: 5.65°C 最低气温: -0.17°C 夜间：晴

成都 更新时间 - 2024-03-06 08:36
2024-03-17 天气: 晴 云量：0.14 最高气温: 22.41°C 最低气温: 11.2°C 夜间：晴

大理 更新时间 - 2024-03-06 08:36
2024-03-09 天气: 晴 云量：0.0 最高气温: 19.53°C 最低气温: 5.7°C 夜间：晴
2024-03-10 天气: 晴 云量：0.0 最高气温: 20.02°C 最低气温: 5.56°C 夜间：晴
2024-03-16 天气: 晴 云量：0.02 最高气温: 21.9°C 最低气温: 7.37°C 夜间：晴

德钦 更新时间 - 2024-03-06 08:36
2024-03-17 天气: 晴 云量：0.17 最高气温: 6.89°C 最低气温: -5.14°C 夜间：晴

丽江 更新时间 - 2024-03-06 08:36
2024-03-09 天气: 晴 云量：0.0 最高气温: 16.59°C 最低气温: 0.68°C 夜间：晴
2024-03-10 天气: 晴 云量：0.08 最高气温: 15.84°C 最低气温: 1.0°C 夜间：晴

```

## How to use

### 1. Destination

The destination is defined in the `destination.json` file, `name` is the destination name, and `location` is the destination coordinates(longitude first, latitude last, separated by commas, decimal format with up to two decimal points, north latitude and east longitude are positive, south latitude and west longitude is negative).

***Note: If you use [HeWeather](https://dev.qweather.com/docs/) as the weather provider, then the GCJ-02 coordinate system should be used in mainland China, and the WGS-84 coordinate system should be used in other areas.***

### 2. Configuration

This project uses [dynaconf](https://github.com/dynaconf/dynaconf) for configuration management. The following are examples and descriptions of `settings.toml`  and `.secrets.toml`.

#### 2.1 settings.toml

```toml
[provider]
weather = "colorful_clouds"
push = "smtp"

[colorful_clouds]
range = "15"
# or
[qweather]
range = "7d"

[smtp]
host = "smtp.example.com"
port = 465
sender = "no-reply@example.com"
receiver = "example@example.com"
```
- **provider**
  - **weather**: Sources of weather forecast information. Options: [colorful_clouds](https://docs.caiyunapp.com/docs/daily), [qweather](https://dev.qweather.com/docs/api/weather/weather-daily-forecast/)
  - **push**: Message push channels. Options: `smtp`

- **colorful_clouds**
  - **range**:  Weather forecast in time range. Options: 1-15

- **qweather**
  - **range**: Weather forecast in time range. Options: `3d`, `7d` for free account.

- **smtp**
  - **host**: The SMTP server.
  - **port**: The SMTP port.
  - **sender**: The email address of the SMTP sender.
  - **receiver**: Optional, the email address of the recipient.

#### 2.2 .secrets.toml

```toml
[colorful_clouds]
dynaconf_merge = true
api_key = ""
# or
[qweather]
dynaconf_merge = true
api_key = ""

[smtp]
dynaconf_merge = true
password = ""
```

- **colorful_clouds**
  - **api_key**:  The API key of Colorful Clouds. You need to create a free project on [Colorful Clouds console](https://platform.caiyunapp.com/dashboard/index) and apply for the API key.

- **qweather**
  - **api_key**: The API key of QWeather. You need to create a free project on [QWeather console](https://console.qweather.com/#/console) and apply for the API key.

- **smtp**
  - **password**: The password of the SMTP sender.


## TODO

- [ ] Allow users to choose their preferred email service provider for notifications
- [ ] Improve email notification content to use html

## Update
- 2023/10/13 Add `Colorful Clouds` as weather provider 
- 2023/08/02 Encountering two consecutive sunny days during the weekend proves to be a rare occurrence, so I revised it to one of the days being sunny.

## License

    Copyright 2023 WangZhiYao
    
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at
    
        http://www.apache.org/licenses/LICENSE-2.0
    
    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
