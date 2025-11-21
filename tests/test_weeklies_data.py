"""Unit tests for WeekliesData."""
import unittest
from unittest.mock import MagicMock, AsyncMock
import sys
from datetime import timedelta
import os

# Mock Home Assistant modules before importing the component
sys.modules["homeassistant"] = MagicMock()
sys.modules["homeassistant.config_entries"] = MagicMock()
sys.modules["homeassistant.const"] = MagicMock()
sys.modules["homeassistant.core"] = MagicMock()
sys.modules["homeassistant.helpers"] = MagicMock()
sys.modules["homeassistant.helpers.storage"] = MagicMock()
sys.modules["homeassistant.helpers.update_coordinator"] = MagicMock()
sys.modules["homeassistant.util"] = MagicMock()
sys.modules["voluptuous"] = MagicMock()

# Now we can import the component classes
# We need to make sure the custom_components path is in sys.path
sys.path.append(os.getcwd())

# Assuming the file structure is standard, we need to point to where custom_components is.
# If running from root, it should be fine.

from custom_components.weeklies import WeekliesData, DAYS_OF_WEEK

class TestWeekliesData(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.hass = MagicMock()
        self.store_mock = AsyncMock()
        self.store_mock.async_load = AsyncMock(return_value=None)
        self.store_mock.async_save = AsyncMock()
        
        # Patch Store in the module or mock the instance
        # Since WeekliesData instantiates Store, we need to mock the class in the module
        with unittest.mock.patch("custom_components.weeklies.Store", return_value=self.store_mock):
            self.weeklies = WeekliesData(self.hass)
            await self.weeklies.async_load()

    async def test_initial_state_empty(self):
        """Test that all days are initialized as empty lists."""
        for day in DAYS_OF_WEEK:
            self.assertIn(day, self.weeklies.data)
            self.assertEqual(self.weeklies.data[day], [])

    async def test_add_item(self):
        """Test adding an item."""
        await self.weeklies.add_item("monday", "Test Item", "mdi:test")
        
        self.assertEqual(len(self.weeklies.data["monday"]), 1)
        item = self.weeklies.data["monday"][0]
        self.assertEqual(item["text"], "Test Item")
        self.assertEqual(item["icon"], "mdi:test")
        self.assertEqual(item["status"], "needs_action")
        
        # Verify save was called
        self.store_mock.async_save.assert_called()

    async def test_add_duplicate_item(self):
        """Test that adding a duplicate item does nothing."""
        await self.weeklies.add_item("monday", "Test Item")
        await self.weeklies.add_item("monday", "Test Item")
        
        self.assertEqual(len(self.weeklies.data["monday"]), 1)

    async def test_remove_item(self):
        """Test removing an item."""
        await self.weeklies.add_item("monday", "Item 1")
        await self.weeklies.add_item("monday", "Item 2")
        
        await self.weeklies.remove_item("monday", "Item 1")
        
        self.assertEqual(len(self.weeklies.data["monday"]), 1)
        self.assertEqual(self.weeklies.data["monday"][0]["text"], "Item 2")

    async def test_remove_non_existent_item(self):
        """Test removing an item that doesn't exist."""
        await self.weeklies.add_item("monday", "Item 1")
        await self.weeklies.remove_item("monday", "Item 99")
        
        self.assertEqual(len(self.weeklies.data["monday"]), 1)

    async def test_invalid_day(self):
        """Test operations on an invalid day."""
        await self.weeklies.add_item("funday", "Party")
        self.assertNotIn("funday", self.weeklies.data)
        
        await self.weeklies.remove_item("funday", "Party")
        # Should not raise error

    async def test_update_status(self):
        """Test updating item status."""
        await self.weeklies.add_item("monday", "Task 1")
        await self.weeklies.update_item_status("monday", "Task 1", "completed")
        
        self.assertEqual(self.weeklies.data["monday"][0]["status"], "completed")

    async def test_load_existing_data(self):
        """Test loading existing data from storage."""
        existing_data = {
            "monday": [{"text": "Existing", "status": "needs_action"}]
        }
        self.store_mock.async_load.return_value = existing_data
        
        # Re-initialize to trigger load
        with unittest.mock.patch("custom_components.weeklies.Store", return_value=self.store_mock):
            weeklies = WeekliesData(self.hass)
            await weeklies.async_load()
            
        self.assertEqual(len(weeklies.data["monday"]), 1)
        self.assertEqual(weeklies.data["monday"][0]["text"], "Existing")
        # Ensure other days are still initialized
        self.assertEqual(weeklies.data["tuesday"], [])

if __name__ == "__main__":
    unittest.main()
