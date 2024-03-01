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
                return bybit.check_price()

    def get_balance(self):
        """Checks the balance of a trader."""
        match self.exchange:
            case 'binance':
                return binance.get_balance()
            case 'bybit':
                return bybit.get_balance()

    def make_limit_order(self, side):
        """Places an order to buy or sell a coin."""
        match self.exchange:
            case 'binance':
                return (binance.buy_coin() if side == 'buy'
                        else binance.sell_coin())
            case 'bybit':
                return (bybit.buy_coin() if side == 'buy'
                        else bybit.sell_coin())

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
