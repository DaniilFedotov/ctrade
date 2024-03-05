from decimal import Decimal, ROUND_FLOOR

from exchange import binance, bybit


class InitialTrader:
    def __init__(self, trader_id, exchange, grid):
        self.trader_id = trader_id
        self.exchange = exchange
        self.grid_settings = grid
        self.token = grid['ticker']['token']['name']
        self.currency = grid['ticker']['currency']['name']
        self.ticker = self.token + self.currency

    def check_price(self):
        """Checks the price of a coin."""
        match self.exchange:
            case 'binance':
                return binance.check_price()
            case 'bybit':
                return bybit.check_price(self.ticker)

    def get_balance(self, coin, in_usd=False):
        """Checks the balance of a trader."""
        match self.exchange:
            case 'binance':
                return binance.get_balance()
            case 'bybit':
                return bybit.get_balance(coin, in_usd)

    def create_limit_order(self, side, quantity, price):
        """Places limit order to buy or sell a coin and return order_id."""
        match self.exchange:
            case 'binance':
                return (binance.buy_coin(quantity, price) if side == 'buy'
                        else binance.sell_coin(quantity, price))
            case 'bybit':
                return (bybit.place_order(
                    category='spot',
                    ticker=self.ticker,
                    side=side,
                    order_type='Limit',
                    quantity=quantity,
                    price=price,))

    def create_market_order(self, side, quantity, market_unit):
        """Places market order to buy or sell a coin and return order_id."""
        match self.exchange:
            case 'binance':
                return (binance.buy_coin(quantity) if side == 'buy'
                        else binance.sell_coin(quantity))
            case 'bybit':
                return (bybit.place_order(
                    category='spot',
                    ticker=self.ticker,
                    side=side,
                    order_type='Market',
                    quantity=quantity,
                    market_unit=market_unit,))

    def value_formatting(self, value, parameter):
        decimal_number = Decimal(str(value))
        if parameter == 'price':
            accuracy = '1.' + self.grid_settings['ticker']['price_precision'] * '0'
        elif parameter == 'quantity':
            accuracy = '1.' + self.grid_settings['ticker']['quantity_precision'] * '0'
        else:
            accuracy = '1.0'
        return float(decimal_number.quantize(
            Decimal(accuracy), ROUND_FLOOR))
