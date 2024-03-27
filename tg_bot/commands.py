import datetime

import requests


API_URL = 'http://backend:8000/api'


def start_trading(update, context):
    """Launches the specified bot."""
    command = update['message']['text'].split(' ')
    if len(command) == 2:
        bot_id = int(command[1])
        trader = requests.get(
            f'{API_URL}/traders/{bot_id}/').json()
        if trader['working']:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='This bot is already running.')
        else:
            response = requests.patch(
                f'{API_URL}/traders/{bot_id}/',
                data={'working': True})
            if response.status_code == 200:
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=f'The bot {bot_id} is running.')
            else:
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text='Unexpected error.')
    else:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Bot number not specified.')


def stop_trading(update, context):
    """Stops the specified bot."""
    command = update['message']['text'].split(' ')
    if len(command) == 2:
        bot_id = int(command[1])
        trader = requests.get(
            f'{API_URL}/traders/{bot_id}/').json()
        if trader['working']:
            response = requests.patch(
                f'{API_URL}/traders/{bot_id}/',
                data={'working': False})
            if response.status_code == 200:
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=f'The bot {bot_id} is stopped.')
            else:
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text='Unexpected error.')
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='This bot has already been stopped.')
    else:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Bot number not specified.')


def get_revenue(update, context):
    """Calculates revenue for recent transactions."""
    command = update['message']['text'].split(' ')
    if len(command) == 2:
        num_of_deals = int(command[1])
    else:
        num_of_deals = 5
    deals = requests.get(f'{API_URL}/deals/').json()
    revenue = 0
    for i in range(num_of_deals):
        deal = deals[i]
        if deal['closed']:
            revenue += deal['revenue']
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f'Revenue for the last {num_of_deals} trades: {revenue} USD.')


def get_daily_revenue(update, context):
    """Calculates revenue for today's transactions."""
    deals = requests.get(f'{API_URL}/deals/').json()
    today = datetime.datetime.today()
    revenue = 0
    if update['message']['text'] == '/daily':
        day = 'today'
        for deal in deals:
            if deal['opening_date'] == today.strftime('%Y-%m-%d'):
                if deal['closed']:
                    revenue += deal['revenue']
    else:
        day = 'yesterday'
        yesterday = today - datetime.timedelta(days=1)
        for deal in deals:
            if deal['opening_date'] == yesterday.strftime('%Y-%m-%d'):
                if deal['closed']:
                    revenue += deal['revenue']
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f'Revenue for {day}: {revenue} USD.')


def get_bot_id(update, context):
    """Give the id of a running trading bot."""
    traders = requests.get(f'{API_URL}/traders/').json()
    bot_id = None
    for trader in traders:
        if trader['working']:
            bot_id = trader['id']
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f'Id of a running trading bot: {bot_id}.')
    if bot_id is None:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='No running bots found.')


def get_tickers(update, context):
    """Displays a list of available tickers."""
    tickers = requests.get(f'http://localhost:8000/api/tickers/').json()
    names = ''
    for ticker in tickers:
        names += 'id:' + ticker['id'] + 'name:' + ticker['name'] + '\n'
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f'Available tickers:\n{names}')


def get_grids(update, context):
    """Displays a list of available grids or create a new one."""
    command_list = update['message']['text'].split(' ')
    if len(command_list) == 1:
        grids = requests.get(f'http://localhost:8000/api/grids/').json()
        data = ''
        for grid in grids:
            data += ('id:' + grid['id'] + '\n' +
                     'bottom:' + grid['bottom'] + '\n' +
                     'top:' + grid['top'] + '\n' +
                     'number_of_levels:' + grid['number_of_levels'] + '\n' +
                     'deposit:' + grid['deposit'] + '\n' +
                     'ticker:' + grid['ticker']['name'] + '\n' +
                     '---------------' + '\n')
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f'Created grids: \n{data}')
    elif len(command_list) == 2:
        grid_id = command_list[-1]
        grid = requests.get(f'http://localhost:8000/api/grids/{grid_id}/').json()
        data = ('id:' + grid['id'] + '\n' +
                'bottom:' + grid['bottom'] + '\n' +
                'top:' + grid['top'] + '\n' +
                'number_of_levels:' + grid['number_of_levels'] + '\n' +
                'deposit:' + grid['deposit'] + '\n' +
                'ticker:' + grid['ticker']['name'])
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f'{data}')
    elif len(command_list) == 6:
        grid = {'bottom': float(command_list[-5]),
                'top': float(command_list[-4]),
                'number_of_levels': int(command_list[-3]),
                'deposit': float(command_list[-2]),
                'ticker': int(command_list[-1])}
        requests.post(f'http://localhost:8000/api/grids/', data=grid)
    else:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Wrong command. Read the instructions.')


def get_traders(update, context):
    """Displays a list of available traders or create a new one."""
    command_list = update['message']['text'].split(' ')
    if len(command_list) == 1:
        traders = requests.get(f'http://localhost:8000/api/traders/').json()
        data = ''
        for trader in traders:
            data += ('id:' + trader['id'] + '\n' +
                     'creation_date:' + trader['creation_date'] + '\n' +
                     'working:' + trader['working'] + '\n' +
                     'initial_deposit:' + trader['initial_deposit'] + '\n' +
                     'current_deposit:' + trader['current_deposit'] + '\n' +
                     'market:' + trader['market'] + '\n' +
                     'exchange:' + trader['exchange'] + '\n' +
                     'grid:' + trader['grid'] + '\n' +
                     '---------------' + '\n')
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f'Created grids: \n{data}')
    elif len(command_list) == 2:
        trader_id = command_list[-1]
        trader = requests.get(f'http://localhost:8000/api/traders/{trader_id}/').json()
        data = ('id:' + trader['id'] + '\n' +
                'creation_date:' + trader['creation_date'] + '\n' +
                'working:' + trader['working'] + '\n' +
                'initial_deposit:' + trader['initial_deposit'] + '\n' +
                'current_deposit:' + trader['current_deposit'] + '\n' +
                'market:' + trader['market'] + '\n' +
                'exchange:' + trader['exchange'] + '\n' +
                'grid:' + trader['grid'])
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f'{data}')
    elif len(command_list) == 3:
        trader = {'exchange': command_list[-2],
                  'grid': int(command_list[-1])}
        requests.post(f'http://localhost:8000/api/traders/', data=trader)
    else:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Wrong command. Read the instructions.')
