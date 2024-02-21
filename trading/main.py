import time
import requests

from core import classes
from strategy import grid_trading


SLEEPTIME_SEC = 60


def check_activity():
    """Checks the status of trading bots."""
    traders = requests.get('http://localhost:8000/api/traders/').json()
    for trader in traders:
        if trader['working']:
            trading_bot = classes.InitialTrader(
                trader_id=trader['id'],
                token=trader['token'],
                currency=trader['currency'],
                exchange=trader['exchange'])
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
