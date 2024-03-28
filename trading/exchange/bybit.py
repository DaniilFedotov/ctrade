import logging
import os
import sys

from dotenv import load_dotenv
from pybit.unified_trading import HTTP


load_dotenv()

BYBIT_API_KEY = os.getenv('BYBIT_API_KEY')
BYBIT_SECRET_KEY = os.getenv('BYBIT_SECRET_KEY')

session = HTTP(
    testnet=False,
    api_key=BYBIT_API_KEY,
    api_secret=BYBIT_SECRET_KEY
)


def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[logging.FileHandler(f'{__name__}.log', mode='a'),
                  logging.StreamHandler(stream=sys.stdout)]
    )


def get_balance(coin=None, in_usd=False):
    """Gets the absolute and relative balance of the coin."""
    logging.debug('Get balance (bybit)')
    balance = session.get_wallet_balance(
        accountType='UNIFIED',
        coin=coin,
    )
    if coin:
        qty = float(balance['result']['list'][0]['coin'][0]['equity'])
        qty_usd = float(balance['result']['list'][0]['coin'][0]['usdValue'])
        return qty_usd if in_usd else qty
    else:
        return float(balance['result']['list'][0]['totalEquity'])


def check_price(symbol):
    """Checks the price of the specified coin."""
    logging.debug('Check price (bybit)')
    tickers = session.get_tickers(
        category='spot',
        symbol=symbol
    )
    price = tickers['result']['list'][0]['lastPrice']
    return float(price)


def place_order(category, ticker, side,  order_type,
                quantity, price=None, market_unit=None):
    """Places an order and gives its ID."""
    logging.debug('Place order (bybit)')
    placed_order = session.place_order(
        category=category,
        symbol=ticker,
        side='Buy' if side == 'buy' else 'Sell',
        orderType=order_type,
        qty=str(quantity),
        price=str(price),
        marketUnit=market_unit,)
    return placed_order['result']['orderId']


def get_open_orders(category, order_id):
    """Receives information about an open order by ID."""
    logging.debug('Get open orders (bybit)')
    order_info = session.get_open_orders(
        category=category,
        orderId=order_id,)
    return order_info['result']['list']


def get_order_history(category, order_id):
    """Receives information about a closed order by ID."""
    logging.debug('Get order history (bybit)')
    order_info = session.get_order_history(
        category=category,
        orderId=order_id,)
    return order_info['result']['list']


def cancel_all_orders():
    """Cancels all placed orders."""
    logging.debug('Cancels all orders (bybit)')
    session.cancel_all_orders(category='spot')
