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
    for i in range(0, num_of_deals):
        deal = deals.json()[i]
        if deal['closed']:
            revenue += deal['revenue']
    context.bot.send_message(
        chat_id=chat.id,
        text=f'Revenue for the last {num_of_deals} trades: {revenue}.')


def get_daily_profit(update, context):
    chat = update.effective_chat
    print(f'update: {update}')
    print(f'context: {context}')
    context.bot.send_message(chat_id=chat.id, text='Some daily profit.')
