"""API client for Hisense TV."""

import logging
import time
import aiohttp

from .const import (
    LOGIN_URL,
    DEVICE_INFO_URL,
    STATUS_MAP,
    LOGIN_DISTRIBUTE_ID,
    DEVICE_DISTRIBUTE_ID,
)

_LOGGER = logging.getLogger(__name__)


class HisenseTVApi:
    """Hisense TV API client."""

    def __init__(self, phone: str, password: str, device_id: str) -> None:
        """Initialize the API client."""
        self._phone = phone
        self._password = password
        self._device_id = device_id
        self._token: str | None = None
        self._session: aiohttp.ClientSession | None = None

    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create aiohttp session."""
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()
        return self._session

    async def close(self) -> None:
        """Close the session."""
        if self._session and not self._session.closed:
            await self._session.close()

    async def login(self) -> bool:
        """Login to Hisense cloud and get token."""
        session = await self._get_session()
        timestamp = int(time.time() * 1000)

        params = {
            "lastUpdateTime": "0",
            "version": "1.0",
            "deviceType": "2",
            "appType": "100",
            "versionCode": "101",
            "_": str(timestamp),
        }

        payload = {
            "deviceType": "1",
            "distributeId": LOGIN_DISTRIBUTE_ID,
            "loginName": self._phone,
            "serverCode": "9501",
            "signature": self._password,
        }

        headers = {
            "Content-Type": "application/json;charset=utf-8",
        }

        try:
            async with session.post(
                LOGIN_URL, params=params, json=payload, headers=headers
            ) as resp:
                if resp.status != 200:
                    _LOGGER.error("Login failed with status %s", resp.status)
                    return False

                data = await resp.json()
                _LOGGER.debug("Login response: %s", data)

                if "data" in data and "tokenInfo" in data["data"]:
                    self._token = data["data"]["tokenInfo"]["token"]
                    _LOGGER.info("Login successful, token obtained")
                    return True
                else:
                    _LOGGER.error("Login response missing token: %s", data)
                    return False

        except Exception as e:
            _LOGGER.error("Login error: %s", e)
            return False

    async def get_device_status(self, retry: bool = True) -> dict | None:
        """Get device status."""
        if not self._token:
            if not await self.login():
                return None

        session = await self._get_session()
        timestamp = int(time.time() * 1000)

        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        }

        payload = {
            "_t": timestamp,
            "accessToken": self._token,
            "deviceIds": [self._device_id],
            "version": "1.2.20.3",
            "deviceType": 3,
            "type": 1,
            "deviceid": "ha_integration",
            "distributeId": DEVICE_DISTRIBUTE_ID,
            "sign": "",
            "appKey": "commonweb",
        }

        try:
            async with session.post(
                DEVICE_INFO_URL, json=payload, headers=headers
            ) as resp:
                if resp.status != 200:
                    _LOGGER.error("Get device status failed with status %s", resp.status)
                    # Token might be expired, try to re-login and retry
                    self._token = None
                    if retry:
                        _LOGGER.info("Retrying after re-login...")
                        return await self.get_device_status(retry=False)
                    return None

                data = await resp.json()
                _LOGGER.debug("Device status response: %s", data)

                if "data" in data and len(data["data"]) > 0:
                    device_data = data["data"][0]
                    # API 返回的 status 可能是字符串，需要转换为整数
                    try:
                        status_code = int(device_data.get("status", -1))
                    except (ValueError, TypeError):
                        status_code = -1
                    return {
                        "status": status_code,
                        "status_text": STATUS_MAP.get(status_code, "未知"),
                        "raw": device_data,
                    }
                else:
                    _LOGGER.error("Device status response missing data: %s", data)
                    # Token might be expired, try to re-login and retry
                    self._token = None
                    if retry:
                        _LOGGER.info("Retrying after re-login...")
                        return await self.get_device_status(retry=False)
                    return None

        except Exception as e:
            _LOGGER.error("Get device status error: %s", e)
            self._token = None
            return None
