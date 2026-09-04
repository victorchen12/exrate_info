# 汇率监控项目（已终止）

本项目已于 2026-09-04 终止。GitHub Actions 自动任务已停用，不再通过 GitHub 定时获取汇率数据，也不再向飞书发送通知。

## 当前状态

- 原工作流 `.github/workflows/exrate-monitor.yml` 已停用并保留为 `.github/workflows/exrate-monitor.yml.disabled`。
- `exrate_monitor/` 下的业务代码和 `tests/` 仅作为历史留存，不再安排运行或维护。
- 不要在 GitHub Actions 中重新启用或手动运行该任务。

## 历史说明

项目原本使用 Frankfurter 公共 API 获取 `CNY -> KRW` 汇率，并通过飞书自定义机器人发送通知。相关环境变量、运行方式和测试依赖仅保留在历史代码中，当前不再使用。
