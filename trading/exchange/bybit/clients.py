from pybit.unified_trading import HTTP

from config import BYBIT_API_KEY, BYBIT_SECRET_KEY


session = HTTP(
    testnet=False,
    api_key=BYBIT_API_KEY,
    api_secret=BYBIT_SECRET_KEY
)


class BybitClient:
    """Client for bybit operations."""
    def __init__(self, category: str = "spot", account_type: str = "UNIFIED"):
        self.category = category
        self.account_type = account_type

    def get_balance(self, coin: str | None = None, in_usd: bool = False):
        """Gets the absolute and relative balance of the coin."""
        balance = session.get_wallet_balance(
            accountType=self.account_type,
            coin=coin
        )
        if coin:
            qty = float(balance["result"]["list"][0]["coin"][0]["equity"])
            qty_usd = float(balance["result"]["list"][0]["coin"][0]["usdValue"])
            return qty_usd if in_usd else qty
        return float(balance["result"]["list"][0]["totalEquity"])

    def check_price(self, symbol: str):
        """Checks the price of the specified coin."""
        tickers = session.get_tickers(
            category=self.category,
            symbol=symbol
        )
        return float(tickers["result"]["list"][0]["lastPrice"])

    def place_order(self, symbol: str, side: str,  order_type: str, quantity: float,
                    price: float | None = None, market_unit: str | None = None):
        """Places an order and gives its ID."""
        placed_order = session.place_order(
            category=self.category,
            symbol=symbol,
            side="Buy" if side == "buy" else "Sell",
            orderType=order_type,
            qty=str(quantity),
            price=str(price),
            marketUnit=market_unit
        )
        return placed_order["result"]["orderId"]

    def get_open_orders(self, order_id: str):
        """Receives information about an open order by ID."""
        order_info = session.get_open_orders(
            category=self.category,
            orderId=order_id
        )
        return order_info["result"]["list"]

    def get_order_history(self, order_id: str):
        """Receives information about a closed order by ID."""
        order_info = session.get_order_history(
            category=self.category,
            orderId=order_id
        )
        return order_info["result"]["list"]

    def cancel_all_orders(self):
        """Cancels all placed orders."""
        session.cancel_all_orders(
            category=self.category
        )
