import time
import requests

from core import classes
from strategy.grid_trading import grid_trading


SLEEPTIME_SEC = 60


def check_activity():
    """Checks the status of trading bots."""
    traders = requests.get('http://backend:8000/api/traders/').json()
    for trader in traders:
        if trader['working']:
            trading_bot = classes.InitialTrader(
                trader_id=trader['id'],
                exchange=trader['exchange'],
                grid=trader['grid'])
            return trading_bot
    return None


def main():
    """Bot launch wait function."""
    while True:
        bot = check_activity()
        if bot is not None:
            grid_trading.trading(bot)
        time.sleep(SLEEPTIME_SEC)


if __name__ == '__main__':
    main()
