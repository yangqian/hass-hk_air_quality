# hass-hk_air_quality
Hong Kong Air Quality custom components for home assistant

# How to add to HACS
https://hacs.xyz/docs/faq/custom_repositories/

## What is it
AQI data from Hong Kong Goverment website https://www.aqhi.gov.hk/tc/index.html, current cities including 
| Cities          | 城市  |
| --------------- | --- |
| Central/Western | 中西區 |
| Southern        | 南區  |
| Eastern         | 東區  |
| Kwun Tong       | 觀塘  |
| Sham Shui Po    | 深水埗 |
| Kwai Chung      | 葵涌  |
| Tsuen Wan       | 荃灣  |
| Tseung Kwan O   | 將軍澳 |
| Yuen Long       | 元朗  |
| Tuen Mun        | 屯門  |
| Tung Chung      | 東涌  |
| Tai Po          | 大埔  |
| Sha Tin         | 沙田  |
| North           | 北區  |
| Tap Mun         | 塔門  |

measures includes
AQHI, NO2, O3, SO2, PM10, PM2.5

AQHI、二氧化氮、臭氧、二氧化硫、PM10、PM2.5

## Data Scraper source
Despite documents say the APIs are provided, I did not find them anywhere.
Pulls data from https://www.aqhi.gov.hk/js/data/past_24_pollutant.js acusing regular expression matching.

## APIs seem to be outdated
* https://github.com/sammyfung/hkaqhi
* https://www.weather.org.hk/aqi.html
* https://github.com/hongkongkiwi/node-hongkong-pollution
