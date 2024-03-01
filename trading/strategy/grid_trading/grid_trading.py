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
    levels = requests.get(
        f'http://backend:8000/api/traders/{trading_bot.trader_id}/'
    ).json()['grid']['levels']
    while grid_status:
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
    step = ((grid['top'] - grid['bottom']) /
            (grid['number_of_levels'] - 1))
    step = bot.value_formatting(step, 'price')
    requests.patch(f'http://backend:8000/api/grids/{grid["id"]}/', data={'step': step})
    if grid['number_of_levels'] % 2 == 0:
        middle = (grid['top'] + grid['bottom']) / 2
        middle = bot.value_formatting(middle, 'price')
        # Ошибочное суждение
        quantity_per_order = (grid['deposit'] / grid['number_of_levels']) * 0.98
        quantity_per_order = bot.value_formatting(quantity_per_order, 'quantity')
        levels = []
        for ind in range(int(grid['number_of_levels'] / 2)):
            selling_price = middle + (0.5 + ind) * step
            selling_price = bot.value_formatting(selling_price, 'price')
            purchase_price = middle - (0.5 + ind) * step
            purchase_price = bot.value_formatting(purchase_price, 'price')
            "Выставить ордер на покупку, на продажу, получить их id"
            sell_order_id = 50 * ind  # временно
            buy_order_id = 60 * ind  # временно
            sell_level = {'side': 'sell',
                          'order_id': sell_order_id,
                          'price': selling_price,
                          'quantity': quantity_per_order,
                          'grid': grid['id']}
            buy_level = {'side': 'buy',
                         'order_id': buy_order_id,
                         'price': purchase_price,
                         'quantity': quantity_per_order,
                         'grid': grid['id']}
            levels.append(sell_level)
            levels.append(buy_level)
        for level in levels:
            requests.post(f'http://backend:8000/api/levels/', data=level)
        return True
