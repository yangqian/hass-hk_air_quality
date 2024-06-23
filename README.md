# hass-hk_air_quality
Hong Kong Air Quality custom components for home assistant

## What is it
AQI data from Hong Kong Goverment website https://www.aqhi.gov.hk/tc/index.html, including 
AQHI, NO2, O3, SO2, PM10, PM2.5
AQHI、二氧化氮、臭氧、二氧化硫、PM10、PM2.5

## Data Scraper source
Despite the document says it provides an API, I did not find it anywhere.
Pulls data from https://www.aqhi.gov.hk/js/data/past_24_pollutant.js using grep
