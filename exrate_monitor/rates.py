from dataclasses import dataclass, field
from datetime import datetime, timezone

import requests

from exrate_monitor.config import AppConfig


class RateApiError(RuntimeError):
    """Raised when Frankfurter returns an unusable response."""


@dataclass(frozen=True)
class RateResult:
    base: str
    quote: str
    amount: float
    rate: float
    fetched_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


def fetch_rate(config: AppConfig) -> RateResult:
    try:
        response = requests.get(
            f"https://api.frankfurter.dev/v2/rate/{config.base}/{config.quote}",
            timeout=15,
        )
        if response.status_code >= 400:
            try:
                error_payload = response.json()
            except ValueError:
                error_payload = {}
            message = error_payload.get("message") or error_payload.get("error") or response.text
            raise RateApiError(f"Exchange-rate API failed: {message}")
        response.raise_for_status()
        payload = response.json()
    except requests.RequestException as exc:
        raise RateApiError(f"Failed to call exchange-rate API: {exc}") from exc
    except ValueError as exc:
        raise RateApiError("Exchange-rate API returned invalid JSON") from exc

    if not isinstance(payload, dict):
        raise RateApiError("Exchange-rate API returned an invalid response body")

    if "rate" not in payload:
        raise RateApiError("Exchange-rate API response missing rate")

    try:
        rate = float(payload["rate"]) * config.amount
    except (TypeError, ValueError) as exc:
        raise RateApiError("Exchange-rate API result is not a number") from exc

    return RateResult(
        base=config.base,
        quote=config.quote,
        amount=config.amount,
        rate=rate,
    )
