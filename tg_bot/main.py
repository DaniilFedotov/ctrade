import os

from telegram import Bot
from telegram.ext import Updater, Filters, MessageHandler, CommandHandler
from dotenv import load_dotenv

from commands import stop_trading, get_revenue, get_daily_profit


load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

HELP_TEXT = (f'Bot is running. You can use the following commands:'
             f'/stop - stopping current trading;'
             f'/profit - get current profit;'
             f'/daily - get profit for the last day;')

bot = Bot(token=TELEGRAM_TOKEN)
updater = Updater(token=TELEGRAM_TOKEN)


def get_help(update, context):
    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id, text=HELP_TEXT)


def main():
    updater.dispatcher.add_handler(CommandHandler('stop', stop_trading))
    updater.dispatcher.add_handler(CommandHandler('revenue', get_revenue))
    updater.dispatcher.add_handler(CommandHandler('daily', get_daily_profit))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, get_help))
    updater.start_polling(poll_interval=1.0)
    updater.idle()


if __name__ == '__main__':
    main()
