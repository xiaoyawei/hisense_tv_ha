"""Constants for Hisense TV integration."""

DOMAIN = "hisense_tv"

# API endpoints
LOGIN_URL = "https://portal-account.hismarttv.com/mobile/signon"
DEVICE_INFO_URL = "https://public-wxtv.hismarttv.com/mobiletv/device/deviceInfo"

# API parameters
LOGIN_DISTRIBUTE_ID = "2001"
DEVICE_DISTRIBUTE_ID = 1001

# Config keys
CONF_PHONE = "phone"
CONF_PASSWORD = "password"
CONF_DEVICE_ID = "device_id"
CONF_SCAN_INTERVAL = "scan_interval"

# Defaults
DEFAULT_SCAN_INTERVAL = 60  # seconds

# Device status mapping
STATUS_MAP = {
    0: "关机",
    1: "开机",
}
