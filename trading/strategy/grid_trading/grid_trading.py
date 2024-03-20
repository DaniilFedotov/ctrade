import sys
import logging
import time
import requests


CHECK_TIME_SEC = 60
SAFETY_FACTOR = 1.02
MINIMUM_ORDER_SIZE = 5
API_URL = 'http://backend:8000/api'


def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[logging.FileHandler(f'{__name__}.log', mode='a'),
                  logging.StreamHandler(stream=sys.stdout)]
    )


def trading(trading_bot):
    """Main trading function."""
    logging.debug('Start trading')
    trader = requests.get(
        f'{API_URL}/traders/{trading_bot.trader_id}/'
    ).json()
    if not trader['initial_deposit']:
        logging.debug('Get initial_deposit')
        balance = trading_bot.get_balance()
        requests.patch(f'{API_URL}/traders/{trading_bot.trader_id}/',
                       data={'initial_deposit': balance,
                             'current_deposit': balance})
    grid_installed = trader['grid']['installed']
    if not grid_installed:
        logging.debug('Grid not installed')
        grid_installed = install_grid(trading_bot)
    while grid_installed:
        logging.debug('Start checking orders')
        trader = requests.get(
            f'{API_URL}/traders/{trading_bot.trader_id}/'
        ).json()
        if not trader['working']:
            finish_trading(trading_bot)
            break
        cur_grid = trader['grid']
        levels = trader['grid']['levels']
        for level in levels:
            order_info = trading_bot.get_order(
                category='spot',
                order_id=level['order_id'],
                closed=True,)
            if order_info:
                order_status = order_info[0]['orderStatus']
                if order_status == 'Filled':
                    logging.debug('Find filled order')
                    if level['inverse']:
                        logging.debug('Deal editing')
                        requests.patch(
                            f'{API_URL}/deals/{level["deal"]}/',
                            data={'exit_price': level['price']})
                        level['deal'] = ''
                    else:
                        logging.debug('Deal creating')
                        ticker = trading_bot.grid_settings['ticker']['id']
                        side = 'long' if level['side'] == 'buy' else 'short'
                        deal = {'ticker': ticker,
                                'side': side,
                                'quantity': level['quantity'],
                                'entry_price': level['price'],
                                'trader': trading_bot.trader_id}
                        deal_info = requests.post(
                            f'{API_URL}/deals/',
                            data=deal).json()
                        level['deal'] = deal_info['id']
                    next_price = (
                        level['price'] - cur_grid['step']
                        if level['side'] == 'sell'
                        else level['price'] + cur_grid['step'])
                    next_quantity = trading_bot.value_formatting(
                        cur_grid['order_size'] / next_price, 'quantity')
                    next_level = {
                        'side': 'buy' if level['side'] == 'sell' else 'sell',
                        'order_id': None,
                        'price': next_price,
                        'quantity': next_quantity,
                        'inverse': False if level['inverse'] else True,
                        'deal': level['deal']}
                    order_id = trading_bot.create_limit_order(
                        side=next_level['side'],
                        quantity=next_level['quantity'],
                        price=next_level['price'])
                    next_level['order_id'] = order_id
                    requests.patch(
                        f'{API_URL}/levels/{level["id"]}/',
                        data=next_level)
                    update_deposit(trader, trading_bot)
        time.sleep(CHECK_TIME_SEC)


def install_grid(bot):
    """Places trading grid orders."""
    logging.debug('Create grid')
    balance = bot.get_balance()
    grid = bot.grid_settings
    requests.patch(f'{API_URL}/traders/{bot.trader_id}/',
                   data={'lock': balance - grid['deposit']})
    step = bot.value_formatting(
        ((grid['top'] - grid['bottom']) /
         (grid['number_of_levels'] - 1)), 'price')
    order_size = bot.value_formatting(
        grid['deposit'] / grid['number_of_levels'], 'price')
    requests.patch(
        f'{API_URL}/grids/{grid["id"]}/',
        data={'step': step, 'order_size': order_size})
    if grid['number_of_levels'] % 2 == 0:
        middle = bot.value_formatting(
            (grid['top'] + grid['bottom']) / 2, 'price')
        cur_price = bot.value_formatting(bot.check_price(), 'price')
        levels = []
        for ind in range(int(grid['number_of_levels'] / 2)):
            init_top_price = middle + (0.5 + ind) * step
            init_bottom_price = middle - (0.5 + ind) * step
            right_pos_top = init_top_price >= cur_price
            right_pos_bottom = init_bottom_price < cur_price
            top_price = bot.value_formatting(
                init_top_price if right_pos_top else
                init_top_price - step, 'price')
            bottom_price = bot.value_formatting(
                init_bottom_price if right_pos_bottom else
                init_bottom_price + step, 'price')
            top_quantity = bot.value_formatting(
                order_size / top_price, 'quantity')
            bottom_quantity = bot.value_formatting(
                order_size / bottom_price, 'quantity')
            top_level = {'side': 'sell' if right_pos_top else 'buy',
                         'order_id': None,
                         'price': top_price,
                         'quantity': top_quantity,
                         'inverse': False if right_pos_top else True,
                         'grid': grid['id'],
                         'deal': ''}
            bottom_level = {'side': 'buy' if right_pos_bottom else 'sell',
                            'order_id': None,
                            'price': bottom_price,
                            'quantity': bottom_quantity,
                            'inverse': False if right_pos_bottom else True,
                            'grid': grid['id'],
                            'deal': ''}
            levels.append(top_level)
            levels.append(bottom_level)

        req_token_balance = 0
        for level in levels:
            if level['side'] == 'sell':
                req_token_balance += level['quantity']
            if level['inverse']:
                ticker = grid['ticker']['id']
                init_price = (level['price'] - step
                              if level['side'] == 'sell'
                              else level['price'] + step)
                side = 'long' if level['side'] == 'sell' else 'short'
                deal = {'ticker': ticker,
                        'side': side,
                        'quantity': level['quantity'],
                        'entry_price': init_price,
                        'trader': bot.trader_id}
                deal_info = requests.post(
                    f'{API_URL}/deals/',
                    data=deal).json()
                level['deal'] = deal_info['id']

        token_balance = bot.get_balance(bot.token)
        if token_balance < req_token_balance:
            logging.debug('Not enough tokens')
            required_qty = bot.value_formatting(
                (req_token_balance - token_balance) *
                SAFETY_FACTOR, 'quantity')
            bot.create_market_order(
                side='buy',
                quantity=required_qty,
                market_unit='baseCoin',)
        elif token_balance > req_token_balance:
            logging.debug('Excess tokens')
            excess_qty = bot.value_formatting(
                token_balance - req_token_balance, 'quantity')
            cur_price = bot.value_formatting(bot.check_price(), 'price')
            if excess_qty * cur_price >= MINIMUM_ORDER_SIZE:
                bot.create_market_order(
                    side='sell',
                    quantity=excess_qty,
                    market_unit='baseCoin',)
        else:
            pass

        for level in levels:
            order_id = bot.create_limit_order(
                side=level['side'],
                quantity=level['quantity'],
                price=level['price'])
            level['order_id'] = order_id
            requests.post(f'{API_URL}/levels/', data=level)
        logging.debug('Grid completed')
        return True


def update_deposit(trader, trading_bot):
    """Updates the deposit field for the trader and grid."""
    logging.debug('Update deposit and grid')
    balance = trading_bot.get_balance()
    requests.patch(f'{API_URL}/traders/{trading_bot.trader_id}/',
                   data={'current_deposit': balance})
    grid_deposit = balance - trader['lock']
    grid = trader['grid']
    order_size = trading_bot.value_formatting(
        grid_deposit / grid['number_of_levels'], 'price')
    requests.patch(
        f'{API_URL}/grids/{grid["id"]}/',
        data={'deposit': grid_deposit, 'order_size': order_size})
    trading_bot.grid_settings = requests.get(
        f'{API_URL}/grids/{grid["id"]}/').json()


def finish_trading(trading_bot):
    trading_bot.cancel_all_orders()
    token_balance = trading_bot.value_formatting(
        trading_bot.get_balance(trading_bot.token), 'quantity')
    trading_bot.create_market_order(
        side='sell',
        quantity=token_balance,
        market_unit='baseCoin')
    requests.patch(
        f'{API_URL}/grids/{trading_bot.grid_settings["id"]}/',
        data={'installed': False})
