"""The Weeklies integration."""
from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.storage import Store
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
import voluptuous as vol

from .const import DOMAIN, DAYS_OF_WEEK

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR, Platform.TODO]

STORAGE_VERSION = 1
STORAGE_KEY = "weeklies.data"

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Weeklies from a config entry."""
    data_store = WeekliesData(hass)
    await data_store.async_load()

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="weeklies",
        update_method=data_store.async_update,
        update_interval=timedelta(minutes=1), # Check periodically, but mostly push-driven
    )
    
    # Initial update to set data
    coordinator.async_set_updated_data(data_store.data)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "coordinator": coordinator,
        "data": data_store,
    }

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # Register Services
    async def add_item(call: ServiceCall) -> None:
        """Add an item to a day."""
        day = call.data["day"].lower()
        text = call.data["text"]
        icon = call.data.get("icon")
        await data_store.add_item(day, text, icon)
        await coordinator.async_refresh()

    async def remove_item(call: ServiceCall) -> None:
        """Remove an item from a day."""
        day = call.data["day"].lower()
        text = call.data["text"]
        await data_store.remove_item(day, text)
        await coordinator.async_refresh()

    hass.services.async_register(
        DOMAIN,
        "add_item",
        add_item,
        schema=vol.Schema({
            vol.Required("day"): vol.In(DAYS_OF_WEEK),
            vol.Required("text"): cv.string,
            vol.Optional("icon"): cv.string,
        }),
    )

    hass.services.async_register(
        DOMAIN,
        "remove_item",
        remove_item,
        schema=vol.Schema({
            vol.Required("day"): vol.In(DAYS_OF_WEEK),
            vol.Required("text"): cv.string,
        }),
    )

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(hass, entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok

class WeekliesData:
    """Class to handle storage and management of weekly items."""

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize."""
        self._store = Store(hass, STORAGE_VERSION, STORAGE_KEY)
        self.data = {day: [] for day in DAYS_OF_WEEK}

    async def async_load(self) -> None:
        """Load data from storage."""
        stored = await self._store.async_load()
        if stored:
            # Merge stored data with default structure to ensure all days exist
            for day in DAYS_OF_WEEK:
                if day in stored:
                    self.data[day] = stored[day]

    async def async_save(self) -> None:
        """Save data to storage."""
        await self._store.async_save(self.data)

    async def async_update(self):
        """Return the current data."""
        return self.data

    async def add_item(self, day: str, text: str, icon: str | None = None) -> None:
        """Add an item."""
        if day not in self.data:
            return
        
        # Check for duplicates based on text
        for item in self.data[day]:
            if item["text"] == text:
                return

        self.data[day].append({
            "text": text,
            "icon": icon,
            "status": "needs_action" # For Todo compatibility
        })
        await self.async_save()

    async def remove_item(self, day: str, text: str) -> None:
        """Remove an item."""
        if day not in self.data:
            return
        
        self.data[day] = [item for item in self.data[day] if item["text"] != text]
        await self.async_save()

    async def update_item_status(self, day: str, text: str, status: str) -> None:
        """Update item status (completed/needs_action)."""
        if day not in self.data:
            return
            
        for item in self.data[day]:
            if item["text"] == text:
                item["status"] = status
                break
        await self.async_save()
