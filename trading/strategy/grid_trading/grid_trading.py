import sys
import logging
import time
import requests


CHECK_TIME_SEC = 30


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
        f'http://backend:8000/api/traders/{trading_bot.trader_id}/'
    ).json()
    if not trader['initial_deposit']:
        logging.debug('Get initial_deposit')
        balance = trading_bot.get_balance()
        requests.patch(f'http://backend:8000/api/traders/{trading_bot.trader_id}/',
                       data={'initial_deposit': balance,
                             'current_deposit': balance})
    grid_installed = trader['grid']['installed']
    if not grid_installed:
        logging.debug('Grid not installed')
        grid_installed = install_grid(trading_bot)
    while grid_installed:
        logging.debug('Start checking orders')
        trader = requests.get(
            f'http://backend:8000/api/traders/{trading_bot.trader_id}/'
        ).json()
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
                            f'http://backend:8000/api/deals/{level["deal"]}/',
                            data={'selling_price': 'price'})
                        level['deal'] = ''
                    else:
                        logging.debug('Deal creating')
                        deal = {'ticker': trading_bot.grid_settings['ticker']['id'],
                                'quantity': level['quantity'],
                                'purchase_price': level['price'],
                                'trader': trading_bot.trader_id}
                        deal_info = requests.post(
                            f'http://backend:8000/api/deals/',
                            data=deal).json()
                        level['deal'] = deal_info['id']
                    step = cur_grid['step']
                    next_price = (
                        level['price'] - step
                        if level['side'] == 'sell'
                        else level['price'] + step)
                    order_size = cur_grid['order_size']
                    next_quantity = trading_bot.value_formatting(order_size / next_price, 'quantity')
                    next_level = {'side': 'buy' if level['side'] == 'sell' else 'sell',
                                  'order_id': None,
                                  'price': next_price,
                                  'quantity': next_quantity,
                                  'inverse': False if level['inverse'] else True}
                    order_id = trading_bot.create_limit_order(
                        side=next_level['side'],
                        quantity=next_level['quantity'],
                        price=next_level['price'])
                    next_level['order_id'] = order_id
                    requests.patch(
                        f'http://backend:8000/api/levels/{level["id"]}/',
                        data=next_level)
                    update_deposit(trader, trading_bot)
        time.sleep(CHECK_TIME_SEC)


def install_grid(bot):
    """Places trading grid orders."""
    logging.debug('Create grid')
    balance = bot.get_balance()
    grid = bot.grid_settings
    requests.patch(f'http://backend:8000/api/traders/{bot.trader_id}/',
                   data={'lock': balance - grid['deposit']})
    step = bot.value_formatting(
        ((grid['top'] - grid['bottom']) /
         (grid['number_of_levels'] - 1)), 'price')
    order_size = bot.value_formatting(
        (grid['deposit'] / grid['number_of_levels']) * 0.95, 'price')
    requests.patch(
        f'http://backend:8000/api/grids/{grid["id"]}/',
        data={'step': step, 'order_size': order_size})
    if grid['number_of_levels'] % 2 == 0:
        middle = bot.value_formatting(
            (grid['top'] + grid['bottom']) / 2, 'price')
        cur_price = bot.value_formatting(bot.check_price(), 'price')
        levels = []
        for ind in range(int(grid['number_of_levels'] / 2)):
            initial_top_price = middle + (0.5 + ind) * step
            initial_bottom_price = middle - (0.5 + ind) * step
            right_position_top = initial_top_price >= cur_price
            right_position_bottom = initial_bottom_price < cur_price
            top_price = bot.value_formatting(
                initial_top_price if right_position_top else
                initial_top_price - step, 'price')
            bottom_price = bot.value_formatting(
                initial_bottom_price if right_position_bottom else
                initial_bottom_price + step, 'price')
            top_quantity = bot.value_formatting(
                order_size / top_price, 'quantity')
            bottom_quantity = bot.value_formatting(
                order_size / bottom_price, 'quantity')
            top_level = {'side': 'sell' if right_position_top else 'buy',
                         'order_id': None,
                         'price': top_price,
                         'quantity': top_quantity,
                         'inverse': False if right_position_top else True,
                         'grid': grid['id'],
                         'deal': ''}
            bottom_level = {'side': 'buy' if right_position_bottom else 'sell',
                            'order_id': None,
                            'price': bottom_price,
                            'quantity': bottom_quantity,
                            'inverse': False if right_position_bottom else True,
                            'grid': grid['id'],
                            'deal': ''}
            levels.append(top_level)
            levels.append(bottom_level)

        number_of_sell_levels = 0
        number_of_buy_levels = 0
        for level in levels:
            if level['side'] == 'sell':
                number_of_sell_levels += 1
            else:
                number_of_buy_levels += 1

        req_proportion = number_of_sell_levels / grid['number_of_levels']
        token_balance_usd = bot.get_balance(bot.token, in_usd=True)
        req_token_balance_usd = req_proportion * grid['deposit']
        if token_balance_usd < req_token_balance_usd:
            logging.debug('Not enough tokens')
            difference = req_token_balance_usd - token_balance_usd
            required_qty = bot.value_formatting(
                difference / cur_price, 'quantity')
            bot.create_market_order(
                side='buy',
                quantity=required_qty,
                market_unit='baseCoin',)
        elif token_balance_usd > req_token_balance_usd:
            logging.debug('Excess tokens')
            difference = token_balance_usd - req_token_balance_usd
            excess_qty = bot.value_formatting(
                difference / cur_price, 'quantity')
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
            requests.post(f'http://backend:8000/api/levels/', data=level)
        logging.debug('Grid completed')
        return True


def update_deposit(trader, trading_bot):
    """Updates the deposit field for the trader and grid."""
    logging.debug('Update deposit and grid')
    balance = trading_bot.get_balance()
    requests.patch(f'http://backend:8000/api/traders/{trading_bot.trader_id}/',
                   data={'current_deposit': balance})
    grid_deposit = balance - trader['lock']
    grid = trader['grid']
    order_size = trading_bot.value_formatting(
        (grid_deposit / grid['number_of_levels']) * 0.95, 'price')
    requests.patch(
        f'http://backend:8000/api/grids/{grid["id"]}/',
        data={'deposit': grid_deposit, 'order_size': order_size})
    trading_bot.grid_settings = requests.get(
        f'http://backend:8000/api/grids/{grid["id"]}/').json()
