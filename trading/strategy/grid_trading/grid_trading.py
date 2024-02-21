import time
import requests

import configuration


def trading(trading_bot):
    grid = setup_grid(trading_bot.pair)
    while True:
        pass


def setup_grid(pair):
    grid_parameters = configuration.GRID_SETTINGS[pair]
    delta = round(((grid_parameters['max'] - grid_parameters['min']) /
                   (grid_parameters['number_of_levels'] - 1)),
                  grid_parameters['precision'])
    grid = {}
    if grid_parameters['number_of_levels'] % 2 == 0:
        for ind in range(grid_parameters['number_of_levels'] / 2):
            grid[f'buy{ind}'] = grid_parameters['min'] + delta * ind
        for ind in range(grid_parameters['number_of_levels'] / 2):
            grid[f'sell{ind}'] = grid_parameters['max'] - delta * ind
    return grid
