import os
from dataclasses import dataclass


class ConfigError(RuntimeError):
    """Raised when required configuration is missing or invalid."""


@dataclass(frozen=True)
class AppConfig:
    feishu_webhook_url: str
    feishu_webhook_secret: str
    base: str = "CNY"
    quote: str = "KRW"
    amount: float = 1.0


def _required_env(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise ConfigError(f"Missing required environment variable: {name}")
    return value


def load_config() -> AppConfig:
    amount_raw = os.getenv("EXRATE_AMOUNT", "1").strip()
    try:
        amount = float(amount_raw)
    except ValueError as exc:
        raise ConfigError("EXRATE_AMOUNT must be a number") from exc

    if amount <= 0:
        raise ConfigError("EXRATE_AMOUNT must be greater than 0")

    return AppConfig(
        feishu_webhook_url=_required_env("FEISHU_WEBHOOK_URL"),
        feishu_webhook_secret=_required_env("FEISHU_WEBHOOK_SECRET"),
        base=os.getenv("EXRATE_BASE", "CNY").strip().upper() or "CNY",
        quote=os.getenv("EXRATE_QUOTE", "KRW").strip().upper() or "KRW",
        amount=amount,
    )
