import logging
import time

import requests

from config import BACKEND_URL, SLEEP_TIME_SEC
from core import classes
from strategy.grid_trading import grid_trading
from utils import setup_logging


logger = logging.getLogger(__name__)


def check_activity():
    """Checks the status of trading bots."""
    try:
        traders = requests.get(f"{BACKEND_URL}/api/traders/").json()
        for trader in traders:
            if trader["working"]:
                return classes.InitialTrader(trader)
        return None
    except Exception:
        return None


def main():
    """Bot launch wait function."""
    setup_logging()
    while True:
        logger.debug("Check activity")
        trading_bot = check_activity()
        if trading_bot is not None:
            logger.debug("Start trading")
            grid_trading.trading(trading_bot)
        time.sleep(SLEEP_TIME_SEC)


if __name__ == "__main__":
    main()
