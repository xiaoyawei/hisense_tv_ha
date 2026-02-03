#!/usr/bin/env python3
"""
测试 API 客户端
使用方法: python test_api.py <手机号> <密码> <设备ID>
"""

import sys
import asyncio

# 添加路径以导入自定义组件
sys.path.insert(0, "./custom_components")

from hisense_tv.api import HisenseTVApi


async def test_api(phone: str, password: str, device_id: str):
    print("=" * 50)
    print("海信电视 API 测试")
    print("=" * 50)

    api = HisenseTVApi(phone, password, device_id)

    # 测试登录
    print("\n[1] 测试登录...")
    login_ok = await api.login()
    if login_ok:
        print("    ✓ 登录成功")
    else:
        print("    ✗ 登录失败")
        await api.close()
        return False

    # 测试获取设备状态
    print("\n[2] 测试获取设备状态...")
    status = await api.get_device_status()
    if status:
        print("    ✓ 获取成功")
        print(f"    状态: {status['status_text']}")
        print(f"    状态码: {status['status']}")
        if "raw" in status:
            raw = status["raw"]
            print(f"    设备名: {raw.get('deviceName', 'N/A')}")
            print(f"    型号: {raw.get('model', 'N/A')}")
    else:
        print("    ✗ 获取失败")
        await api.close()
        return False

    await api.close()
    print("\n" + "=" * 50)
    print("✓ 所有测试通过！插件应该可以正常工作")
    print("=" * 50)
    return True


def main():
    if len(sys.argv) != 4:
        print("用法: python test_api.py <手机号> <密码> <设备ID>")
        print("示例: python test_api.py 15512345678 mypassword 86100300000100100000060c5fe97655")
        sys.exit(1)

    phone, password, device_id = sys.argv[1], sys.argv[2], sys.argv[3]
    asyncio.run(test_api(phone, password, device_id))


if __name__ == "__main__":
    main()
