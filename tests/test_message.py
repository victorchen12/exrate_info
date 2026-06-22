from datetime import datetime
from zoneinfo import ZoneInfo

from exrate_monitor.message import build_feishu_text
from exrate_monitor.rates import RateResult


def test_build_feishu_text_includes_rate_beijing_time_and_source():
    fetched_at = datetime(2026, 6, 22, 1, 15, tzinfo=ZoneInfo("UTC"))
    rate = RateResult(
        base="CNY",
        quote="KRW",
        amount=1.0,
        rate=189.123456,
        fetched_at=fetched_at,
    )

    text = build_feishu_text(rate)

    assert "1 CNY = 189.123456 KRW" in text
    assert "北京时间: 2026-06-22 09:15" in text
    assert "数据源: Frankfurter" in text
