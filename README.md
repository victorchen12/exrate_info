# 汇率监控与飞书推送

Python 3.11 项目，用 GitHub Actions 定时从 Frankfurter 公共接口获取 `CNY -> KRW` 汇率并推送到飞书自定义机器人。汇率接口不需要 API key。

## GitHub Secrets

在仓库 `Settings -> Secrets and variables -> Actions -> Secrets` 中配置：

- `FEISHU_WEBHOOK_URL`: 飞书自定义机器人的 webhook URL
- `FEISHU_WEBHOOK_SECRET`: 飞书机器人签名密钥

可选变量可放在 Actions Variables 中：

- `EXRATE_BASE`: 默认 `CNY`
- `EXRATE_QUOTE`: 默认 `KRW`
- `EXRATE_AMOUNT`: 默认 `1`

## 定时执行

工作流文件为 `.github/workflows/exrate-monitor.yml`。

默认 cron 是：

```cron
15 1,5,10 * * *
```

GitHub Actions 使用 UTC 时间，对应北京时间每日 `09:15 / 13:15 / 18:15`。

## 手动运行

在 GitHub 仓库的 `Actions -> Exchange Rate Monitor -> Run workflow` 手动触发。

本地也可以运行：

```bash
python -m pip install .
python -m exrate_monitor.main
```

本地运行前需要先设置上述环境变量。

## API 注意事项

当前使用 Frankfurter 公共 API，不需要申请 key。默认每天 3 次，约每月 90 到 93 次请求；如果未来接口限制发生变化，可以减少 cron 频率或切换数据源。

## 测试

开发依赖安装后运行：

```bash
python -m pip install ".[dev]"
python -m pytest
```
