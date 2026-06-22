import pytest
import responses

from exrate_monitor.config import AppConfig
from exrate_monitor.rates import RateApiError, fetch_rate


def make_config() -> AppConfig:
    return AppConfig(
        feishu_webhook_url="https://open.feishu.cn/webhook",
        feishu_webhook_secret="feishu-secret",
        base="CNY",
        quote="KRW",
        amount=1.0,
    )


@responses.activate
def test_fetch_rate_parses_successful_response():
    responses.add(
        responses.GET,
        "https://api.frankfurter.dev/v2/rate/CNY/KRW",
        json={"date": "2026-06-22", "base": "CNY", "quote": "KRW", "rate": 189.1234},
        status=200,
    )

    result = fetch_rate(make_config())

    assert result.base == "CNY"
    assert result.quote == "KRW"
    assert result.amount == 1.0
    assert result.rate == 189.1234
    request = responses.calls[0].request
    assert request.url == "https://api.frankfurter.dev/v2/rate/CNY/KRW"


@responses.activate
def test_fetch_rate_calculates_converted_amount_locally():
    responses.add(
        responses.GET,
        "https://api.frankfurter.dev/v2/rate/CNY/KRW",
        json={"date": "2026-06-22", "base": "CNY", "quote": "KRW", "rate": 189.1234},
        status=200,
    )
    config = AppConfig(
        feishu_webhook_url="https://open.feishu.cn/webhook",
        feishu_webhook_secret="feishu-secret",
        base="CNY",
        quote="KRW",
        amount=5.0,
    )

    result = fetch_rate(config)

    assert result.amount == 5.0
    assert result.rate == pytest.approx(945.617)


@responses.activate
def test_fetch_rate_fails_when_api_returns_error_status():
    responses.add(
        responses.GET,
        "https://api.frankfurter.dev/v2/rate/CNY/KRW",
        json={"message": "unsupported currency"},
        status=422,
    )

    with pytest.raises(RateApiError, match="unsupported currency"):
        fetch_rate(make_config())


@responses.activate
def test_fetch_rate_fails_when_result_missing():
    responses.add(
        responses.GET,
        "https://api.frankfurter.dev/v2/rate/CNY/KRW",
        json={"date": "2026-06-22", "base": "CNY", "quote": "KRW"},
        status=200,
    )

    with pytest.raises(RateApiError, match="rate"):
        fetch_rate(make_config())
