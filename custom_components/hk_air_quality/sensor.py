import logging
import re
import asyncio
import aiohttp

from datetime import timedelta
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.entity import DeviceInfo
from .const import DOMAIN, CONF_CITY, CONF_MEASURE
from homeassistant.helpers.update_coordinator import CoordinatorEntity


_LOGGER = logging.getLogger(__name__)
async def async_setup_entry(hass, entry, async_add_entities):
    config_id = entry.entry_id
    coordinator = hass.data[DOMAIN][config_id]["coordinator"]
    city = hass.data[DOMAIN][config_id]["city"]
    measure = hass.data[DOMAIN][config_id]["measure"]
    async_add_entities([HKAirQualitySensor(coordinator, city, measure, config_id)], True)

class HKAirQualitySensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, city, measure, config_id: str):
        super().__init__(coordinator)
        self.config_id = config_id
        self._city = city
        self._measure = measure
        self._name = f"{city} {measure}"

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            identifiers={(DOMAIN, self.config_id)},
            name="Air Pollution",
            manufacturer="Hong Kong",
            suggested_area="Patio",
        )
    @property
    def unique_id(self) -> str:
        return f"{DOMAIN}_{self._city}_{self._measure}"
    @property
    def name(self):
        return self._name

    @property
    def state(self):
        content = self.coordinator.data
        pattern = fr'"stationNameEN":"{self._city}".*?"{self._measure}":"([.\d]+)"'
        match = re.search(pattern, content)

        if match:
            _LOGGER.warning(f"{self._measure} data found for {self._city} is {match.group(1)}")
            return match.group(1)
        else:
            _LOGGER.warning(f"No {self._measure} data found for {self._city}")
            return None

    @property
    def unit_of_measurement(self):
        return "µg/m³"
