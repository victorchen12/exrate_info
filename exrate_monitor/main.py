import sys

from exrate_monitor.config import ConfigError, load_config
from exrate_monitor.feishu import FeishuError, send_feishu_message
from exrate_monitor.message import build_feishu_text
from exrate_monitor.rates import RateApiError, fetch_rate


def main() -> int:
    try:
        config = load_config()
        rate = fetch_rate(config)
        text = build_feishu_text(rate)
        send_feishu_message(config, text)
    except (ConfigError, RateApiError, FeishuError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
