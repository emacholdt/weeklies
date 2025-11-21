"""Sensor platform for Weeklies."""
from __future__ import annotations

from datetime import datetime, timedelta

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import dt as dt_util

from .const import DOMAIN, DAYS_OF_WEEK

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Weeklies sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]

    entities = []
    # Per-day sensors
    for day in DAYS_OF_WEEK:
        entities.append(WeeklyDaySensor(coordinator, day))
    
    # Today and Tomorrow sensors
    entities.append(WeeklyRelativeSensor(coordinator, "today"))
    entities.append(WeeklyRelativeSensor(coordinator, "tomorrow"))

    async_add_entities(entities)


class WeeklyDaySensor(CoordinatorEntity, SensorEntity):
    """Sensor for a specific day's tasks."""

    def __init__(self, coordinator, day: str) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._day = day
        self._attr_name = f"Weeklies {day.capitalize()}"
        self._attr_unique_id = f"weeklies_sensor_{day}"
        self._attr_icon = "mdi:calendar-check"

    @property
    def native_value(self) -> int:
        """Return the count of items."""
        items = self.coordinator.data.get(self._day, [])
        # Count only active items? Or all? Let's count all for now, or maybe just active.
        # Requirement was "reminders for jobs", usually implies active jobs.
        # But if we use Todo list to check them off, maybe we only want to see 'needs_action'.
        # Let's return count of 'needs_action' items.
        return sum(1 for item in items if item.get("status", "needs_action") == "needs_action")

    @property
    def extra_state_attributes(self) -> dict[str, any]:
        """Return the state attributes."""
        items = self.coordinator.data.get(self._day, [])
        return {"items": items}


class WeeklyRelativeSensor(CoordinatorEntity, SensorEntity):
    """Sensor for Today or Tomorrow."""

    def __init__(self, coordinator, relative_day: str) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._relative_day = relative_day
        self._attr_name = f"Weeklies {relative_day.capitalize()}"
        self._attr_unique_id = f"weeklies_sensor_{relative_day}"
        self._attr_icon = "mdi:calendar-today" if relative_day == "today" else "mdi:calendar-arrow-right"

    @property
    def _target_day(self) -> str:
        """Get the target day name (e.g., 'monday')."""
        now = dt_util.now()
        if self._relative_day == "tomorrow":
            now = now + timedelta(days=1)
        return now.strftime("%A").lower()

    @property
    def native_value(self) -> int:
        """Return the count of items."""
        day = self._target_day
        items = self.coordinator.data.get(day, [])
        return sum(1 for item in items if item.get("status", "needs_action") == "needs_action")

    @property
    def extra_state_attributes(self) -> dict[str, any]:
        """Return the state attributes."""
        day = self._target_day
        items = self.coordinator.data.get(day, [])
        return {
            "items": items,
            "day": day
        }
