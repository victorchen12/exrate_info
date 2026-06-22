from pathlib import Path

import yaml


def test_workflow_has_schedule_and_manual_dispatch():
    workflow = yaml.safe_load(Path(".github/workflows/exrate-monitor.yml").read_text())

    assert workflow["on"]["schedule"] == [{"cron": "15 1,5,10 * * *"}]
    assert "workflow_dispatch" in workflow["on"]


def test_workflow_runs_monitor_module():
    workflow_text = Path(".github/workflows/exrate-monitor.yml").read_text()

    assert "python -m exrate_monitor.main" in workflow_text
    assert "FEISHU_WEBHOOK_URL" in workflow_text
    assert "FEISHU_WEBHOOK_SECRET" in workflow_text
