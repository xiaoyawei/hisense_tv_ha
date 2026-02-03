#!/usr/bin/env python3
"""
海信电视设备ID获取工具
使用方法: python get_device_id.py
"""

import requests
import time
import json

# ============ 请修改以下信息 ============
PHONE = "你的手机号"
PASSWORD = "你的密码"
# ======================================

LOGIN_URL = "https://portal-account.hismarttv.com/mobile/signon"
DEVICE_LIST_URL = "https://public-wxtv.hismarttv.com/mobiletv/device/deviceList"


def login(phone: str, password: str) -> dict | None:
    """登录获取token和用户信息"""
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
        "distributeId": "2001",
        "loginName": phone,
        "serverCode": "9501",
        "signature": password,
    }

    headers = {
        "Content-Type": "application/json;charset=utf-8",
    }

    try:
        resp = requests.post(LOGIN_URL, params=params, json=payload, headers=headers)
        data = resp.json()

        if "data" in data and "tokenInfo" in data["data"]:
            print("✓ 登录成功!")
            return data["data"]
        else:
            print(f"✗ 登录失败: {data.get('message', data)}")
            return None
    except Exception as e:
        print(f"✗ 登录异常: {e}")
        return None


def get_device_list(token: str) -> list | None:
    """获取设备列表"""
    timestamp = int(time.time() * 1000)

    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    }

    payload = {
        "_t": timestamp,
        "accessToken": token,
        "version": "1.2.20.3",
        "deviceType": 3,
        "type": 1,
        "deviceid": "get_device_tool",
        "distributeId": 1001,
        "sign": "",
        "appKey": "commonweb",
    }

    try:
        resp = requests.post(DEVICE_LIST_URL, json=payload, headers=headers)
        data = resp.json()

        if "data" in data:
            return data["data"]
        else:
            print(f"获取设备列表失败: {data}")
            return None
    except Exception as e:
        print(f"获取设备列表异常: {e}")
        return None


def main():
    if PHONE == "你的手机号" or PASSWORD == "你的密码":
        print("请先修改脚本中的 PHONE 和 PASSWORD 变量!")
        print("然后重新运行: python get_device_id.py")
        return

    print(f"正在登录账号: {PHONE[:3]}****{PHONE[-4:]}")
    print("-" * 50)

    # 登录
    login_data = login(PHONE, PASSWORD)
    if not login_data:
        return

    token = login_data["tokenInfo"]["token"]

    # 获取设备列表
    print("\n正在获取设备列表...")
    devices = get_device_list(token)

    if not devices:
        print("未找到设备，请确认账号已绑定电视")
        return

    print(f"\n找到 {len(devices)} 个设备:")
    print("=" * 60)

    for i, device in enumerate(devices, 1):
        print(f"\n【设备 {i}】")
        print(f"  设备ID:   {device.get('deviceId', 'N/A')}")
        print(f"  设备名称: {device.get('deviceName', 'N/A')}")
        print(f"  型号:     {device.get('model', 'N/A')}")
        print(f"  MAC:      {device.get('mac', 'N/A')}")
        print(f"  状态:     {'开机' if device.get('status') == 1 else '关机'}")

    print("\n" + "=" * 60)
    print("请复制上面的 设备ID 用于 Home Assistant 配置")


if __name__ == "__main__":
    main()
