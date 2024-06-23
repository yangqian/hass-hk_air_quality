from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from datetime import timedelta
import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN, CONF_CITY, CONF_MEASURE
from .config_flow import HKAirQualityConfigFlow

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    hass.data.setdefault(DOMAIN, {})

    async def async_update_data():
        url = "https://www.aqhi.gov.hk/js/data/past_24_pollutant.js"
        session = async_get_clientsession(hass)

        async with session.get(url) as response:
            content = await response.text()
            return content

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=DOMAIN,
        update_interval=timedelta(hours=1),
        update_method=async_update_data,
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id] = {
        "coordinator": coordinator,
        "city": entry.data[CONF_CITY],
        "measure": entry.data[CONF_MEASURE],
    }

    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "sensor")
    )

    return True
