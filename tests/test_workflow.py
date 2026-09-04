from pathlib import Path


ACTIVE_WORKFLOW = Path(".github/workflows/exrate-monitor.yml")
DISABLED_WORKFLOW = Path(".github/workflows/exrate-monitor.yml.disabled")


def test_exchange_rate_workflow_is_disabled():
    assert not ACTIVE_WORKFLOW.exists()
    assert DISABLED_WORKFLOW.exists()


def test_disabled_workflow_is_preserved_for_reference():
    workflow_text = DISABLED_WORKFLOW.read_text()

    assert "python -m exrate_monitor.main" in workflow_text
