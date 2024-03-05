import time
import requests


CHECK_TIME_SEC = 30


def trading(trading_bot):
    """Main trading function."""
    trader = requests.get(
        f'http://backend:8000/api/traders/{trading_bot.trader_id}/'
    ).json()
    grid_installed = trader['grid']['installed']
    if not grid_installed:
        grid_installed = install_grid(trading_bot)
    while grid_installed:
        levels = requests.get(
            f'http://backend:8000/api/traders/{trading_bot.trader_id}/'
        ).json()['grid']['levels']
        for level in levels:
            order_status = 'FILLED'  # Реализовать проверку через API биржи
            if order_status == 'FILLED':
                new_level = level
                new_level['side'] = 'buy' if level['side'] == 'sell' else 'sell'
                new_level['order_id'] = 3140310  # Новый id после выставления ордера
                new_level['price'] = 4143143  # Рассчитывать новую цену отнимая или прибавляя дельту, не забыть форматирование
                new_level['quantity'] = 25335  # Рассчитывать новое количество, не забыть форматирование
                new_level['inverse'] = False if level['inverse'] else True
                requests.patch(
                    f'http://backend:8000/api/levels/{new_level["id"]}/',
                    data={
                        'side': new_level['side'],
                        'order_id': new_level['order_id'],
                        'price': new_level['price'],
                        'quantity': new_level['quantity'],
                        'inverse': new_level['inverse']
                    })
        time.sleep(CHECK_TIME_SEC)


def install_grid(bot):
    """Places trading grid orders."""
    grid = bot.grid_settings
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
            top_price = bot.value_formatting(
                middle + (0.5 + ind) * step, 'price')
            bottom_price = bot.value_formatting(
                middle - (0.5 + ind) * step, 'price')
            top_quantity = bot.value_formatting(
                order_size / top_price, 'quantity')
            bottom_quantity = bot.value_formatting(
                order_size / bottom_price, 'quantity')
            top_level = {'side': 'sell' if top_price >= cur_price else 'buy',
                         'order_id': None,
                         'price': top_price,
                         'quantity': top_quantity,
                         'grid': grid['id'],
                         'inverse': False if top_price >= cur_price else True}
            bottom_level = {'side': 'buy' if bottom_price < cur_price else 'sell',
                            'order_id': None,
                            'price': bottom_price,
                            'quantity': bottom_quantity,
                            'grid': grid['id'],
                            'inverse': False if bottom_price < cur_price else True}
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
            difference = req_token_balance_usd - token_balance_usd
            required_qty = bot.value_formatting(
                difference / cur_price, 'quantity')
            bot.create_market_order(
                side='buy',
                quantity=required_qty,
                market_unit='baseCoin',)
        elif token_balance_usd > req_token_balance_usd:
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
            level['order_id'] = order_id['result']['orderId']
            requests.post(f'http://backend:8000/api/levels/', data=level)
        return True
