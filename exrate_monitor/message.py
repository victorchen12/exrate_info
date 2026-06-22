from zoneinfo import ZoneInfo

from exrate_monitor.rates import RateResult


def _format_amount(amount: float) -> str:
    return str(int(amount)) if amount.is_integer() else f"{amount:g}"


def build_feishu_text(rate: RateResult) -> str:
    beijing_time = rate.fetched_at.astimezone(ZoneInfo("Asia/Shanghai"))
    amount = _format_amount(rate.amount)
    return "\n".join(
        [
            "汇率监控",
            f"{amount} {rate.base} = {rate.rate:.6f} {rate.quote}",
            f"北京时间: {beijing_time:%Y-%m-%d %H:%M}",
            "数据源: Frankfurter",
        ]
    )
