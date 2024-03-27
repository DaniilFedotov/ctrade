import os

from telegram import Bot
from telegram.ext import Updater, Filters, MessageHandler, CommandHandler
from dotenv import load_dotenv

from commands import (start_trading, stop_trading, get_revenue,
                      get_daily_revenue, get_bot_id, get_tickers,
                      grids, traders)


load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

HELP_TEXT = ('Bot is running. You can use the following commands:\n'
             '/start x - start existing trading bot with id x;\n'
             '/stop x - stop trading bot with id x;\n'
             '/revenue x - get revenue for the last x trades (default - 5);\n'
             '/daily - get revenue for today;\n'
             '/id - get the id of a running bots;\n'
             '/help - get help message.')

bot = Bot(token=TELEGRAM_TOKEN)
updater = Updater(token=TELEGRAM_TOKEN)


def get_help(update, context):
    """Gives information about available commands."""
    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id, text=HELP_TEXT)


def main():
    """Distributes received commands."""
    updater.dispatcher.add_handler(CommandHandler('start', start_trading))
    updater.dispatcher.add_handler(CommandHandler('stop', stop_trading))
    updater.dispatcher.add_handler(CommandHandler('revenue', get_revenue))
    updater.dispatcher.add_handler(CommandHandler('daily', get_daily_revenue))
    updater.dispatcher.add_handler(CommandHandler('yesterday', get_daily_revenue))
    updater.dispatcher.add_handler(CommandHandler('id', get_bot_id))
    updater.dispatcher.add_handler(CommandHandler('tickers', get_tickers))
    updater.dispatcher.add_handler(CommandHandler('grids', grids))
    updater.dispatcher.add_handler(CommandHandler('traders', traders))
    updater.dispatcher.add_handler(CommandHandler('help', get_help))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, get_help))
    updater.start_polling(poll_interval=1.0)
    updater.idle()


if __name__ == '__main__':
    main()
