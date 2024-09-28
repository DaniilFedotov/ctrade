import logging
import time

from config import CHECK_TIME_SEC
from core.classes import TradingBot
from core.managers import TraderManager
from strategy.grid_trading import grid_trading, utils
from utils import setup_logging


logger = logging.getLogger(__name__)


def check_activity():
    """Checks the status of trading bots."""
    try:
        traders = TraderManager.get_traders()
        for trader in traders:
            if trader["working"]:
                logger.debug("Trader have status working")
                return TradingBot(trader=trader)
        return None
    except Exception as exc:
        logger.debug(f"Exc: {exc}")
        return None


def main():
    """Bot launch wait function."""
    setup_logging()
    while True:
        logger.debug("Check activity")
        trading_bot = check_activity()
        if trading_bot is not None:
            try:
                grid_trading.trading_process(trading_bot=trading_bot)
            except Exception as exc:
                logger.debug(f"Exc: {exc}")
            finally:
                utils.finish_trading(trading_bot=trading_bot)
        time.sleep(CHECK_TIME_SEC)


if __name__ == "__main__":
    main()
