import logging
from decimal import Decimal, ROUND_FLOOR

from core.utils import get_exchange_client
from exchange import binance, bybit


logger = logging.getLogger(__name__)


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
                logger.debug("Check price")
                return bybit.check_price(self.ticker)

    def get_balance(self, coin=None, in_usd=False):
        """Checks the balance of a trader."""
        match self.exchange:
            case "binance":
                return binance.get_balance()
            case "bybit":
                logger.debug("Get balance")
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
                logger.debug("Create limit order")
                return bybit.place_order(
                    category="spot",  # Del
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
                logger.debug("Create market order")
                return bybit.place_order(
                    category="spot",  # Del
                    ticker=self.ticker,
                    side=side,
                    order_type="Market",
                    quantity=quantity,
                    market_unit=market_unit
                )

    def get_order(self, category, order_id, closed=False): # D cat
        """Receives order information by ID."""
        match self.exchange:
            case "binance":
                pass
            case "bybit":
                if closed:
                    logger.debug("Get order (closed)")
                    return bybit.get_order_history(
                        category=category,  # D
                        order_id=order_id
                    )
                logger.debug("Get order")
                return bybit.get_open_orders(
                    category=category,  # D
                    order_id=order_id
                )

    def value_formatting(self, value, parameter):
        """Formats numbers according to exchange requirements."""
        logger.debug("Value formatting")
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
        logger.debug("Cancel orders")
        bybit.cancel_all_orders()


class TradingBot:
    def __init__(self, trader: dict):
        self.trader_id = trader["id"]
        self.exchange_client = get_exchange_client(trader["exchange"])()
        self.grid_settings = trader["grid"]
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
