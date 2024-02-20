import datetime

import requests


def stop_trading(update, context):
    """Stops a specific bot."""
    chat = update.effective_chat
    command = update['message']['text'].split(' ')
    if len(command) == 2:
        bot_id = int(command[1])
        trader = requests.get(
            f'http://localhost:8000/api/traders/{bot_id}/')
        if trader.json()['working']:
            response = requests.patch(
                f'http://localhost:8000/api/traders/{bot_id}/',
                data={'working': False})
            if response.status_code == 200:
                context.bot.send_message(
                    chat_id=chat.id,
                    text=f'The bot {bot_id} is stopped.')
            else:
                context.bot.send_message(
                    chat_id=chat.id,
                    text=f'Unexpected error.')
        else:
            context.bot.send_message(
                chat_id=chat.id,
                text=f'This bot has already been stopped.')
    else:
        context.bot.send_message(
            chat_id=chat.id,
            text=f'Bot number not specified.')


def get_revenue(update, context):
    """Calculates revenue for recent transactions."""
    chat = update.effective_chat
    command = update['message']['text'].split(' ')
    if len(command) == 2:
        num_of_deals = int(command[1])
    else:
        num_of_deals = 5
    deals = requests.get('http://localhost:8000/api/deals/')
    revenue = 0
    for i in range(num_of_deals):
        deal = deals.json()[i]
        if deal['closed']:
            revenue += deal['revenue']
    context.bot.send_message(
        chat_id=chat.id,
        text=f'Revenue for the last {num_of_deals} trades: {revenue} USD.')


def get_daily_revenue(update, context):
    """Calculates revenue for today's transactions."""
    chat = update.effective_chat
    deals = requests.get('http://localhost:8000/api/deals/')
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    revenue = 0
    for deal in deals.json():
        if deal['opening_date'] == today:
            if deal['closed']:
                revenue += deal['revenue']
        else:
            break
    context.bot.send_message(
        chat_id=chat.id,
        text=f'Revenue for today: {revenue} USD.')
