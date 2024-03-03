import time
import requests


CHECK_TIME_SEC = 30


def trading(trading_bot):
    """Main trading function."""
    trader = requests.get(
        f'http://backend:8000/api/traders/{trading_bot.trader_id}/'
    ).json()
    grid_status = trader['grid']['installed']
    if not grid_status:
        grid_status = install_grid(trading_bot)
    while grid_status:
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
        (grid['deposit'] / grid['number_of_levels']) * 0.98, 'price')
    requests.patch(
        f'http://backend:8000/api/grids/{grid["id"]}/',
        data={'step': step, 'order_size': order_size})
    if grid['number_of_levels'] % 2 == 0:
        middle = bot.value_formatting(
            (grid['top'] + grid['bottom']) / 2, 'price')
        levels = []
        for ind in range(int(grid['number_of_levels'] / 2)):
            selling_price = bot.value_formatting(
                middle + (0.5 + ind) * step, 'price')
            purchase_price = bot.value_formatting(
                middle - (0.5 + ind) * step, 'price')
            sell_quantity = bot.value_formatting(
                order_size / selling_price, 'quantity')
            buy_quantity = bot.value_formatting(
                order_size / purchase_price, 'quantity')
            "Выставить ордер на покупку, на продажу, получить их id"
            #sell_order_id = bot.create_limit_order(
            # side='sell',
            # quantity=sell_quantity,
            # price=selling_price)[] # Как то вернуть id
            #buy_order_id = bot.create_limit_order(
            # side='buy',
            # quantity=buy_quantity,
            # price=purchase_price)[] # Как то вернуть id
            sell_order_id = 50 * ind  # временно
            buy_order_id = 60 * ind  # временно
            sell_level = {'side': 'sell',
                          'order_id': sell_order_id,
                          'price': selling_price,
                          'quantity': sell_quantity,
                          'grid': grid['id']}
            buy_level = {'side': 'buy',
                         'order_id': buy_order_id,
                         'price': purchase_price,
                         'quantity': buy_quantity,
                         'grid': grid['id']}
            levels.append(sell_level)
            levels.append(buy_level)
        for level in levels:
            requests.post(f'http://backend:8000/api/levels/', data=level)
        return True
