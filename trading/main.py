import logging
import sys
import time

import requests

from core import classes
from strategy.grid_trading import grid_trading


SLEEPTIME_SEC = 60


def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(f"{__name__}.log", mode="a"),
            logging.StreamHandler(stream=sys.stdout)
        ]
    )


def check_activity():
    """Checks the status of trading bots."""
    try:
        traders = requests.get("http://backend:8000/api/traders/").json()
        for trader in traders:
            if trader["working"]:
                return classes.InitialTrader(trader)
        return None
    except Exception:
        return None


def main():
    """Bot launch wait function."""
    while True:
        logging.debug("Check activity")
        trading_bot = check_activity()
        if trading_bot is not None:
            logging.debug("Start trading")
            grid_trading.trading(trading_bot)
        time.sleep(SLEEPTIME_SEC)


if __name__ == "__main__":
    main()
