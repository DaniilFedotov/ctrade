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


def get_balance(currency):
    """Finds out account balance."""
    balance = session.get_wallet_balance(
        accountType='UNIFIED',
        coin=currency
    )
    return float(balance['result']['list'][0]['coin'][0]['equity'])


def check_price(symbol):
    """Checks the price of the specified coin."""
    tickers = session.get_tickers(
        category='spot',
        coin='USDC'
    )
    price = None
    for ticker in tickers:
        if ticker['symbol'] == symbol:
            price = float(ticker['lastPrice'])
    return price


def place_order(quantity, price, ticker, category, order_type, side):
    """Places an order and gives its ID."""
    placed_order = session.place_order(
        category=category,
        symbol=ticker,
        side='Buy' if side == 'buy' else 'Sell',
        orderType=order_type,
        qty=str(quantity),
        price=str(price)
    )
    return placed_order['result']['orderId']
