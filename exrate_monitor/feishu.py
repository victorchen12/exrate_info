import base64
import hashlib
import hmac
import time

import requests

from exrate_monitor.config import AppConfig


class FeishuError(RuntimeError):
    """Raised when Feishu webhook delivery fails."""


def build_feishu_signature(secret: str, timestamp: str) -> str:
    string_to_sign = f"{timestamp}\n{secret}"
    digest = hmac.new(string_to_sign.encode("utf-8"), b"", digestmod=hashlib.sha256).digest()
    return base64.b64encode(digest).decode("utf-8")


def send_feishu_message(config: AppConfig, text: str) -> None:
    timestamp = str(int(time.time()))
    payload = {
        "timestamp": timestamp,
        "sign": build_feishu_signature(config.feishu_webhook_secret, timestamp),
        "msg_type": "text",
        "content": {"text": text},
    }

    try:
        response = requests.post(config.feishu_webhook_url, json=payload, timeout=15)
        response.raise_for_status()
        body = response.json()
    except requests.RequestException as exc:
        raise FeishuError(f"Failed to call Feishu webhook: {exc}") from exc
    except ValueError as exc:
        raise FeishuError("Feishu webhook returned invalid JSON") from exc

    code = body.get("StatusCode", body.get("code", 0))
    if code != 0:
        message = body.get("StatusMessage") or body.get("msg") or body.get("message") or body
        raise FeishuError(f"Feishu webhook failed: {message}")
