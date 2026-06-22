import base64
import hashlib
import hmac

import pytest
import responses

from exrate_monitor.config import AppConfig
from exrate_monitor.feishu import FeishuError, build_feishu_signature, send_feishu_message


def make_config() -> AppConfig:
    return AppConfig(
        feishu_webhook_url="https://open.feishu.cn/open-apis/bot/v2/hook/token",
        feishu_webhook_secret="feishu-secret",
        base="CNY",
        quote="KRW",
        amount=1.0,
    )


def test_build_feishu_signature_matches_hmac_sha256_rule():
    timestamp = "1700000000"
    secret = "feishu-secret"
    expected = base64.b64encode(
        hmac.new(f"{timestamp}\n{secret}".encode(), b"", digestmod=hashlib.sha256).digest()
    ).decode()

    assert build_feishu_signature(secret, timestamp) == expected


@responses.activate
def test_send_feishu_message_posts_signed_text_payload(monkeypatch):
    monkeypatch.setattr("exrate_monitor.feishu.time.time", lambda: 1700000000)
    responses.add(
        responses.POST,
        "https://open.feishu.cn/open-apis/bot/v2/hook/token",
        json={"StatusCode": 0, "StatusMessage": "success"},
        status=200,
    )

    send_feishu_message(make_config(), "hello")

    payload = responses.calls[0].request.body.decode()
    assert '"msg_type": "text"' in payload
    assert '"text": "hello"' in payload
    assert '"timestamp": "1700000000"' in payload
    assert '"sign":' in payload


@responses.activate
def test_send_feishu_message_fails_on_webhook_error():
    responses.add(
        responses.POST,
        "https://open.feishu.cn/open-apis/bot/v2/hook/token",
        json={"StatusCode": 19024, "StatusMessage": "bad sign"},
        status=200,
    )

    with pytest.raises(FeishuError, match="bad sign"):
        send_feishu_message(make_config(), "hello")
