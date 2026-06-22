from zoneinfo import ZoneInfo

from exrate_monitor.rates import RateResult


def _format_amount(amount: float) -> str:
    return str(int(amount)) if amount.is_integer() else f"{amount:g}"


def build_feishu_text(rate: RateResult) -> str:
    beijing_time = rate.fetched_at.astimezone(ZoneInfo("Asia/Shanghai"))
    unit_rate = rate.rate / rate.amount
    base_needed = 100 / unit_rate
    return "\n".join(
        [
            "汇率监控",
            f"100 {rate.quote} = {base_needed:.6f} {rate.base}",
            f"参考: {_format_amount(rate.amount)} {rate.base} = {rate.rate:.6f} {rate.quote}",
            f"北京时间: {beijing_time:%Y-%m-%d %H:%M}",
            "数据源: Frankfurter",
        ]
    )
