import logging
import time

from config import CHECK_TIME_SEC
from core.classes import TradingBot
from core.managers import TraderManager
from strategy.grid_trading import grid_trading
from utils import setup_logging


logger = logging.getLogger(__name__)


def check_activity():
    """Checks the status of trading bots."""
    try:
        traders = TraderManager.get_traders()
        for trader in traders:
            if trader["working"]:
                return TradingBot(trader=trader)
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
            grid_trading.trading(trading_bot=trading_bot)
        time.sleep(CHECK_TIME_SEC)


if __name__ == "__main__":
    main()
