from exchange import binance, bybit


class InitialTrader:
    def __init__(self, trader_id, token, currency, exchange):
        self.trader_id = trader_id
        self.token = token
        self.currency = currency
        self.pair = token + currency
        self.exchange = exchange

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

    def buy_coin(self):
        """Places an order to buy a coin."""
        match self.exchange:
            case 'binance':
                return binance.buy_coin()
            case 'bybit':
                return bybit.buy_coin()

    def sell_coin(self):
        """Places an order to sell a coin."""
        match self.exchange:
            case 'binance':
                return binance.sell_coin()
            case 'bybit':
                return bybit.sell_coin()
