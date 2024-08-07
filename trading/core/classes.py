import logging
import sys
from decimal import Decimal, ROUND_FLOOR

from exchange import binance, bybit


def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(f"{__name__}.log", mode="a"),
            logging.StreamHandler(stream=sys.stdout)
        ]
    )


class InitialTrader:
    def __init__(self, trader):
        self.trader_id = trader["id"]
        self.exchange = trader["exchange"]
        self.grid_settings = trader["grid"]
        self.token = self.grid_settings["ticker"]["token"]["name"]
        self.currency = self.grid_settings["ticker"]["currency"]["name"]
        self.ticker = self.token + self.currency

    def check_price(self):
        """Checks the price of a coin."""
        match self.exchange:
            case "binance":
                return binance.check_price()
            case "bybit":
                logging.debug("Check price")
                return bybit.check_price(self.ticker)

    def get_balance(self, coin=None, in_usd=False):
        """Checks the balance of a trader."""
        match self.exchange:
            case "binance":
                return binance.get_balance()
            case "bybit":
                logging.debug("Get balance")
                return bybit.get_balance(
                    coin=coin,
                    in_usd=in_usd
                )

    def create_limit_order(self, side, quantity, price):
        """Places limit order to buy or sell a coin and return order_id."""
        match self.exchange:
            case "binance":
                return (binance.buy_coin(quantity, price) if side == "buy"
                        else binance.sell_coin(quantity, price))
            case "bybit":
                logging.debug("Create limit order")
                return bybit.place_order(
                    category="spot",
                    ticker=self.ticker,
                    side=side,
                    order_type="Limit",
                    quantity=quantity,
                    price=price
                )

    def create_market_order(self, side, quantity, market_unit):
        """Places market order to buy or sell a coin and return order_id."""
        match self.exchange:
            case "binance":
                return (binance.buy_coin(quantity) if side == "buy"
                        else binance.sell_coin(quantity))
            case "bybit":
                logging.debug("Create market order")
                return bybit.place_order(
                    category="spot",
                    ticker=self.ticker,
                    side=side,
                    order_type="Market",
                    quantity=quantity,
                    market_unit=market_unit
                )

    def get_order(self, category, order_id, closed=False):
        """Receives order information by ID."""
        match self.exchange:
            case "binance":
                pass
            case "bybit":
                if closed:
                    logging.debug("Get order (closed)")
                    return bybit.get_order_history(
                        category=category,
                        order_id=order_id
                    )
                logging.debug("Get order")
                return bybit.get_open_orders(
                    category=category,
                    order_id=order_id
                )

    def value_formatting(self, value, parameter):
        """Formats numbers according to exchange requirements."""
        logging.debug("Value formatting")
        decimal_number = Decimal(str(value))
        if parameter == "price":
            accuracy = ("1." + "0" *
                        self.grid_settings["ticker"]["price_precision"])
        elif parameter == "quantity":
            accuracy = ("1." + "0" *
                        self.grid_settings["ticker"]["quantity_precision"])
        else:
            accuracy = "1.0"
        return float(
            decimal_number.quantize(Decimal(accuracy), ROUND_FLOOR)
        )

    def cancel_all_orders(self):
        """Cancels all orders."""
        logging.debug("Cancel orders")
        bybit.cancel_all_orders()
