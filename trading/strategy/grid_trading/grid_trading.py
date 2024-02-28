import time
import requests


def trading(trading_bot):
    status = install_grid(trading_bot)
    while status:
        pass


def install_grid(bot):
    grid = bot.grid_settings
    delta = (grid['top'] - grid['bottom']) / (grid['number_of_levels'] - 1)
    delta = bot.value_formatting(delta, 'price')
    levels = {}
    if bot.grid['number_of_levels'] % 2 == 0:
        for ind in range(grid['number_of_levels']):
            levels[f'{ind}'] = grid['top'] - delta * ind

        return True
