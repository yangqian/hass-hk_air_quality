import voluptuous as vol

from homeassistant import config_entries
from .const import DOMAIN, CONF_CITY, CONF_MEASURE
from homeassistant.helpers.aiohttp_client import async_get_clientsession
import homeassistant.helpers.config_validation as cv
import re

class HKAirQualityConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title=user_input[CONF_CITY], data=user_input)
        cities = await self.get_available_cities()
        measure_list=["aqhi","NO2","O3","SO2","CO","PM10","PM25"]
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_CITY, default="Tai Po"): vol.In(cities),
                    vol.Required(CONF_MEASURE, default=["PM25"]): 
                    cv.multi_select(
                        {
                            measure: measure
                            for measure in measure_list
                        }
                    )
                }
            ),
        )
    
    async def get_available_cities(self):
        url = "https://www.aqhi.gov.hk/js/data/past_24_pollutant.js"
        session = async_get_clientsession(self.hass)

        async with session.get(url) as response:
            content = await response.text()
            pattern = r'"StationNameEN":"([^"]+)"'
            cities = sorted(set(re.findall(pattern, content)))
            return cities
