"""Sensor platform for Hisense TV."""

from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import DOMAIN, CONF_DEVICE_ID, CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Hisense TV sensor from config entry."""
    api = hass.data[DOMAIN][entry.entry_id]
    device_id = entry.data[CONF_DEVICE_ID]
    scan_interval = entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)

    async def async_update_data():
        """Fetch data from API."""
        data = await api.get_device_status()
        if data is None:
            raise UpdateFailed("Failed to get device status")
        return data

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="hisense_tv",
        update_method=async_update_data,
        update_interval=timedelta(seconds=scan_interval),
    )

    await coordinator.async_config_entry_first_refresh()

    async_add_entities([HisenseTVSensor(coordinator, device_id, entry)])


class HisenseTVSensor(CoordinatorEntity, SensorEntity):
    """Hisense TV status sensor."""

    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        device_id: str,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._device_id = device_id
        self._attr_unique_id = f"hisense_tv_{device_id}_status"
        self._attr_name = "海信电视状态"
        self._attr_icon = "mdi:television"

    @property
    def native_value(self) -> str | None:
        """Return the state of the sensor."""
        if self.coordinator.data:
            return self.coordinator.data.get("status_text")
        return None

    @property
    def extra_state_attributes(self) -> dict:
        """Return extra state attributes."""
        if self.coordinator.data and "raw" in self.coordinator.data:
            raw = self.coordinator.data["raw"]
            return {
                "device_id": self._device_id,
                "status_code": self.coordinator.data.get("status"),
                "device_name": raw.get("deviceName"),
                "model": raw.get("model"),
                "mac": raw.get("mac"),
            }
        return {"device_id": self._device_id}
