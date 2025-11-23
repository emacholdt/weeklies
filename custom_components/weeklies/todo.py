"""Todo platform for Weeklies."""
from __future__ import annotations

from typing import Any

from homeassistant.components.todo import (
    TodoItem,
    TodoItemStatus,
    TodoListEntity,
    TodoListEntityFeature,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, DAYS_OF_WEEK
from . import WeekliesData

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Weeklies todo platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    data_store = hass.data[DOMAIN][entry.entry_id]["data"]

    entities = []
    for day in DAYS_OF_WEEK:
        entities.append(WeeklyTodoList(coordinator, data_store, day))

    async_add_entities(entities)


class WeeklyTodoList(CoordinatorEntity, TodoListEntity):
    """A Todo List for a specific day of the week."""

    _attr_supported_features = (
        TodoListEntityFeature.CREATE_TODO_ITEM
        | TodoListEntityFeature.DELETE_TODO_ITEM
        | TodoListEntityFeature.UPDATE_TODO_ITEM
    )

    def __init__(self, coordinator, data_store: WeekliesData, day: str) -> None:
        """Initialize the todo list."""
        super().__init__(coordinator)
        self._data_store = data_store
        self._day = day
        self._attr_name = f"Weeklies {day.capitalize()}"
        self._attr_unique_id = f"weeklies_{day}"

    @property
    def todo_items(self) -> list[TodoItem] | None:
        """Get the items for the todo list."""
        items = []
        day_data = self.coordinator.data.get(self._day, [])
        for item in day_data:
            status = TodoItemStatus.NEEDS_ACTION
            if item.get("status") == "completed":
                status = TodoItemStatus.COMPLETED
            
            items.append(
                TodoItem(
                    summary=item["text"],
                    uid=item["text"], # Using text as UID for simplicity in this context
                    status=status,
                )
            )
        return items

    async def async_create_todo_item(self, item: TodoItem) -> None:
        """Add an item to the todo list."""
        await self._data_store.add_item(self._day, item.summary)
        await self.coordinator.async_refresh()

    async def async_update_todo_item(self, item: TodoItem) -> None:
        """Update an item in the todo list."""
        # We only support updating status (checking off)
        status = "needs_action"
        if item.status == TodoItemStatus.COMPLETED:
            status = "completed"
        
        await self._data_store.update_item_status(self._day, item.uid, status)
        await self.coordinator.async_refresh()

    async def async_delete_todo_items(self, uids: list[str]) -> None:
        """Delete items from the todo list."""
        for uid in uids:
            await self._data_store.remove_item(self._day, uid)
        await self.coordinator.async_refresh()
