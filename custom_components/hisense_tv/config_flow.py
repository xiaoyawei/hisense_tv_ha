"""Config flow for Hisense TV integration."""

from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult

from .api import HisenseTVApi
from .const import (
    DOMAIN,
    CONF_PHONE,
    CONF_PASSWORD,
    CONF_DEVICE_ID,
    CONF_SCAN_INTERVAL,
    DEFAULT_SCAN_INTERVAL,
)

_LOGGER = logging.getLogger(__name__)


class HisenseTVConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Hisense TV."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            # Validate the credentials
            api = HisenseTVApi(
                phone=user_input[CONF_PHONE],
                password=user_input[CONF_PASSWORD],
                device_id=user_input[CONF_DEVICE_ID],
            )

            try:
                if await api.login():
                    # Try to get device status to validate device_id
                    status = await api.get_device_status()
                    await api.close()

                    if status is not None:
                        # Create unique id based on device_id
                        await self.async_set_unique_id(user_input[CONF_DEVICE_ID])
                        self._abort_if_unique_id_configured()

                        return self.async_create_entry(
                            title=f"海信电视 ({user_input[CONF_DEVICE_ID][-8:]})",
                            data=user_input,
                        )
                    else:
                        errors["base"] = "invalid_device"
                else:
                    errors["base"] = "invalid_auth"
            except Exception as e:
                _LOGGER.error("Unexpected error: %s", e)
                errors["base"] = "unknown"
            finally:
                await api.close()

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_PHONE): str,
                    vol.Required(CONF_PASSWORD): str,
                    vol.Required(CONF_DEVICE_ID): str,
                    vol.Optional(
                        CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL
                    ): int,
                }
            ),
            errors=errors,
        )
