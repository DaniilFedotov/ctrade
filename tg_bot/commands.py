def stop_trading(update, context):
    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id, text='Trade stopped.')


def get_profit(update, context):
    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id, text='Some profit.')


def get_daily_profit(update, context):
    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id, text='Some daily profit.')
