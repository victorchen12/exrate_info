import pytest

from exrate_monitor.config import ConfigError, load_config


def test_load_config_uses_required_secrets_and_defaults(monkeypatch):
    monkeypatch.setenv("FEISHU_WEBHOOK_URL", "https://open.feishu.cn/webhook")
    monkeypatch.setenv("FEISHU_WEBHOOK_SECRET", "feishu-secret")
    monkeypatch.delenv("EXRATE_BASE", raising=False)
    monkeypatch.delenv("EXRATE_QUOTE", raising=False)
    monkeypatch.delenv("EXRATE_AMOUNT", raising=False)

    config = load_config()

    assert config.feishu_webhook_url == "https://open.feishu.cn/webhook"
    assert config.feishu_webhook_secret == "feishu-secret"
    assert config.base == "CNY"
    assert config.quote == "KRW"
    assert config.amount == 1.0


def test_load_config_fails_when_required_feishu_url_missing(monkeypatch):
    monkeypatch.delenv("FEISHU_WEBHOOK_URL", raising=False)
    monkeypatch.setenv("FEISHU_WEBHOOK_SECRET", "feishu-secret")

    with pytest.raises(ConfigError, match="FEISHU_WEBHOOK_URL"):
        load_config()


def test_load_config_accepts_optional_currency_and_amount(monkeypatch):
    monkeypatch.setenv("FEISHU_WEBHOOK_URL", "https://open.feishu.cn/webhook")
    monkeypatch.setenv("FEISHU_WEBHOOK_SECRET", "feishu-secret")
    monkeypatch.setenv("EXRATE_BASE", " usd ")
    monkeypatch.setenv("EXRATE_QUOTE", " jpy ")
    monkeypatch.setenv("EXRATE_AMOUNT", "5")

    config = load_config()

    assert config.base == "USD"
    assert config.quote == "JPY"
    assert config.amount == 5.0
