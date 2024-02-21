import time
import requests

from core import classes


SLEEPTIME_SEC = 60


def check_activity():
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
    while True:
        is_active = check_activity()
        if is_active is not None:
            pass
        time.sleep(SLEEPTIME_SEC)


if __name__ == '__main__':
    main()
