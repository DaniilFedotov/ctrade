import datetime

import requests


def stop_trading(update, context):
    chat = update.effective_chat
    print(f'update: {update}')
    print(f'context: {context}')
    context.bot.send_message(chat_id=chat.id, text='Trade stopped.')


def get_revenue(update, context):
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
