# Hisense TV Home Assistant Integration (海信电视)

通过海信云端 API 将海信电视接入 Home Assistant。

## 功能

- 显示电视开关机状态（开机/关机）
- 支持 UI 配置
- 自动刷新状态

## 安装

1. 将 `custom_components/hisense_tv` 文件夹复制到你的 Home Assistant 配置目录下的 `custom_components` 文件夹中

```
config/
  custom_components/
    hisense_tv/
      __init__.py
      api.py
      config_flow.py
      const.py
      manifest.json
      sensor.py
      strings.json
      translations/
        en.json
        zh-Hans.json
```

2. 重启 Home Assistant

3. 在 HA 中添加集成：设置 → 设备与服务 → 添加集成 → 搜索 "Hisense TV"

## 配置参数

| 参数 | 说明 |
|------|------|
| 手机号 | 海信智家 App 登录手机号 |
| 密码 | 海信智家 App 登录密码 |
| 设备ID | 电视的设备ID（32位字符串） |
| 刷新间隔 | 状态刷新间隔，默认60秒 |

## 如何获取设备ID

### 方法1：从海信智家小程序抓包

1. 使用抓包工具（如 Charles、Fiddler）
2. 打开微信海信智家小程序
3. 查看设备信息
4. 在请求中找到 `deviceIds` 字段

### 方法2：从 Node-RED 配置中提取

如果你有 Node-RED 配置，查找 `deviceIds` 字段中的值。

## 实体

安装后会创建一个传感器实体：

- `sensor.hai_xin_dian_shi_zhuang_tai` - 显示 "开机" 或 "关机"

### 额外属性

- `device_id`: 设备ID
- `status_code`: 状态码 (0=关机, 1=开机)
- `device_name`: 设备名称
- `model`: 型号
- `mac`: MAC地址

## 注意事项

- 此集成使用云端 API，需要网络连接
- Token 会自动刷新
- 建议刷新间隔不要设置太短，避免频繁请求
