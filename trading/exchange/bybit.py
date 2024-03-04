import os

from pybit.unified_trading import HTTP
from dotenv import load_dotenv


load_dotenv()

BYBIT_API_KEY = os.getenv('BYBIT_API_KEY')
BYBIT_SECRET_KEY = os.getenv('BYBIT_SECRET_KEY')

session = HTTP(
    testnet=False,
    api_key=BYBIT_API_KEY,
    apy_secret=BYBIT_SECRET_KEY
)


def get_balance():
    pass


def check_price():
    pass


def buy_coin(quantity, price):
    pass


def sell_coin(quantity, price):
    pass
