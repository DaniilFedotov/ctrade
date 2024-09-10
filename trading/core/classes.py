import logging
from decimal import Decimal, ROUND_FLOOR

from core.utils import get_exchange_client


logger = logging.getLogger(__name__)


class TradingBot:
    def __init__(self, trader: dict):
        self.trader_id = trader["id"]
        self.exchange_client = get_exchange_client(trader["exchange"])()
        self.grid = trader["grid"]
        self.trading_pair = TradingPair(trader["grid"]["ticker"])

    def check_price(self):
        """Checks the price of a coin."""
        return self.exchange_client.check_price(self.trading_pair.ticker)

    def get_balance(self, coin: str | None = None, in_usd: bool = False):
        """Checks the balance of a trader."""
        return self.exchange_client.get_balance(
            coin=coin,
            in_usd=in_usd
        )

    def create_limit_order(self, side: str, quantity: float, price: float):
        """Places limit order to buy or sell a coin and return order_id."""
        return self.exchange_client.place_order(
            symbol=self.trading_pair.ticker,
            side=side,
            order_type="Limit",
            quantity=quantity,
            price=price
        )

    def create_market_order(self, side: str, quantity: float, market_unit: str):
        """Places market order to buy or sell a coin and return order_id."""
        return self.exchange_client.place_order(
            symbol=self.trading_pair.ticker,
            side=side,
            order_type="Market",
            quantity=quantity,
            market_unit=market_unit
        )

    def get_order(self, order_id: str, closed: bool = False):
        """Receives order information by ID."""
        if closed:
            return self.exchange_client.get_order_history(order_id=order_id)
        return self.exchange_client.get_open_orders(order_id=order_id)

    def cancel_all_orders(self):
        """Cancels all orders."""
        self.exchange_client.cancel_all_orders()


class TradingPair:
    def __init__(self, ticker: dict):
        self.token = ticker["token"]["name"]
        self.currency = ticker["currency"]["name"]
        self.ticker = ticker["name"]
        self.price_precision = ticker["price_precision"]
        self.quantity_precision = ticker["quantity_precision"]

    def value_formatting(self, value: float, parameter: str):
        """Formats numbers according to exchange requirements."""
        decimal_number = Decimal(str(value))
        if parameter == "price":
            accuracy = ("1." + "0" * self.price_precision)
        elif parameter == "quantity":
            accuracy = ("1." + "0" * self.quantity_precision)
        else:
            accuracy = "1.0"
        return float(decimal_number.quantize(Decimal(accuracy), ROUND_FLOOR))
