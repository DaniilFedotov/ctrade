import os
import datetime

import requests
from dotenv import load_dotenv


load_dotenv()

ADDRESS = os.getenv('ADDRESS')


def start_trading(update, context):
    """Launches the specified bot."""
    command = update['message']['text'].split(' ')
    if len(command) == 2:
        bot_id = int(command[1])
        trader = requests.get(
            f'http://{ADDRESS}:8000/api/traders/{bot_id}/')
        if trader.json()['working']:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f'This bot is already running.')
        else:
            response = requests.patch(
                f'http://{ADDRESS}:8000/api/traders/{bot_id}/',
                data={'working': True})
            if response.status_code == 200:
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=f'The bot {bot_id} is running.')
            else:
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=f'Unexpected error.')
    else:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f'Bot number not specified.')


def stop_trading(update, context):
    """Stops the specified bot."""
    command = update['message']['text'].split(' ')
    if len(command) == 2:
        bot_id = int(command[1])
        trader = requests.get(
            f'http://{ADDRESS}:8000/api/traders/{bot_id}/')
        if trader.json()['working']:
            response = requests.patch(
                f'http://{ADDRESS}:8000/api/traders/{bot_id}/',
                data={'working': False})
            if response.status_code == 200:
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=f'The bot {bot_id} is stopped.')
            else:
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=f'Unexpected error.')
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f'This bot has already been stopped.')
    else:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f'Bot number not specified.')


def get_revenue(update, context):
    """Calculates revenue for recent transactions."""
    command = update['message']['text'].split(' ')
    if len(command) == 2:
        num_of_deals = int(command[1])
    else:
        num_of_deals = 5
    deals = requests.get(f'http://{ADDRESS}:8000/api/deals/')
    revenue = 0
    for i in range(num_of_deals):
        deal = deals.json()[i]
        if deal['closed']:
            revenue += deal['revenue']
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f'Revenue for the last {num_of_deals} trades: {revenue} USD.')


def get_daily_revenue(update, context):
    """Calculates revenue for today's transactions."""
    deals = requests.get(f'http://{ADDRESS}:8000/api/deals/')
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    revenue = 0
    for deal in deals.json():
        if deal['opening_date'] == today:
            if deal['closed']:
                revenue += deal['revenue']
        else:
            break
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f'Revenue for today: {revenue} USD.')


def get_bot_id(update, context):
    """Give the id of a running trading bot."""
    traders = requests.get(f'http://{ADDRESS}:8000/api/traders/')
    bot_id = None
    for trader in traders.json():
        if trader['working']:
            bot_id = trader['id']
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f'Id of a running trading bot: {bot_id}.')
    if bot_id is None:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f'No running bots found.')
