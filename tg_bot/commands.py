import datetime

import requests


API_URL = "http://backend:8000/api"
MSG_MAX_SIZE_PC = 10


def start_trading(update, context):
    """Launches the specified bot."""
    command = update["message"]["text"].split(" ")
    if len(command) == 2:
        bot_id = int(command[1])
        trader = requests.get(
            f"{API_URL}/traders/{bot_id}/"
        ).json()
        if trader["working"]:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="This bot is already running."
            )
        else:
            response = requests.patch(
                f"{API_URL}/traders/{bot_id}/",
                data={"working": True}
            )
            if response.status_code == 200:
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=f"The bot {bot_id} is running."
                )
            else:
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="Unexpected error."
                )
    else:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Bot number not specified."
        )


def stop_trading(update, context):
    """Stops the specified bot."""
    command = update["message"]["text"].split(" ")
    if len(command) == 2:
        bot_id = int(command[1])
        trader = requests.get(
            f"{API_URL}/traders/{bot_id}/"
        ).json()
        if trader["working"]:
            response = requests.patch(
                f"{API_URL}/traders/{bot_id}/",
                data={"working": False}
            )
            if response.status_code == 200:
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=f"The bot {bot_id} is stopped."
                )
            else:
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="Unexpected error."
                )
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="This bot has already been stopped."
            )
    else:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Bot number not specified."
        )


def get_revenue(update, context):
    """Calculates revenue for recent transactions."""
    command = update["message"]["text"].split(" ")
    if len(command) == 2:
        num_of_deals = int(command[1])
    else:
        num_of_deals = 5
    deals = requests.get(f"{API_URL}/deals/").json()
    revenue = 0
    for i in range(num_of_deals):
        deal = deals[i]
        if deal["closed"]:
            revenue += deal["revenue"]
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Revenue for the last {num_of_deals} trades: {revenue} USD."
    )


def get_daily(update, context):
    """Calculates revenue for today's or yesterday's transactions."""
    deals = requests.get(f"{API_URL}/deals/").json()
    today = datetime.datetime.today()
    revenue = 0
    if update["message"]["text"] == "/daily":
        day = "today"
        for deal in deals:
            if (deal["opening_date"] == today.strftime("%Y-%m-%d")
                    and deal["closed"]):
                revenue += deal["revenue"]
    else:
        day = "yesterday"
        yesterday = today - datetime.timedelta(days=1)
        for deal in deals:
            if (deal["opening_date"] == yesterday.strftime("%Y-%m-%d")
                    and deal["closed"]):
                revenue += deal["revenue"]
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Revenue for {day}: {revenue} USD."
    )


def get_bot_id(update, context):
    """Give the id of a running trading bot."""
    traders = requests.get(f"{API_URL}/traders/").json()
    bot_id = None
    for trader in traders:
        if trader["working"]:
            bot_id = trader["id"]
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"Id of a running trading bot: {bot_id}."
            )
    if bot_id is None:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="No running bots found."
        )


def get_tickers(update, context):
    """Displays a list of available tickers."""
    tickers = requests.get(f"{API_URL}/tickers/").json()
    names = ""
    for ticker in tickers:
        names += f"id: {ticker['id']} name: {ticker['name']}\n"
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Available tickers:\n{names}"
    )


def get_grids(update, context):
    """Displays a list of available grids or create a new one."""
    command_list = update["message"]["text"].split(" ")
    if len(command_list) == 1:
        grids = requests.get(f"{API_URL}/grids/").json()
        data = ""
        for i in range(MSG_MAX_SIZE_PC):
            data += (
                f"id: {grids[i]['id']}\n"
                f"bottom: {grids[i]['bottom']}\n"
                f"top: {grids[i]['top']}\n"
                f"number_of_levels: {grids[i]['number_of_levels']}\n"
                f"deposit: {grids[i]['deposit']}\n"
                f"ticker: {grids[i]['ticker']['name']}\n"
                "---------------\n"
            )
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Last {MSG_MAX_SIZE_PC} created grids: \n{data}"
        )
    elif len(command_list) == 2:
        grid_id = command_list[-1]
        grid = requests.get(f"{API_URL}/grids/{grid_id}/").json()
        data = (
            f"id: {grid['id']}\n"
            f"bottom: {grid['bottom']}\n"
            f"top: {grid['top']}\n"
            f"number_of_levels: {grid['number_of_levels']}\n"
            f"deposit: {grid['deposit']}\n"
            f"ticker: {grid['ticker']['name']}"
        )
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"{data}"
        )
    elif len(command_list) == 6:
        grid = {
            "bottom": float(command_list[-5]),
            "top": float(command_list[-4]),
            "number_of_levels": int(command_list[-3]),
            "deposit": float(command_list[-2]),
            "ticker": int(command_list[-1])
        }
        grid_info = requests.post(f"{API_URL}/grids/", data=grid).json()
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Grid created. id: {grid_info['id']}."
        )
    else:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Wrong command. Read the instructions."
        )


def get_traders(update, context):
    """Displays a list of available traders or create a new one."""
    command_list = update["message"]["text"].split(" ")
    if len(command_list) == 1:
        traders = requests.get(f"{API_URL}/traders/").json()
        data = ""
        for i in range(MSG_MAX_SIZE_PC):
            data += (
                f"id: {traders[i]['id']}\n"
                f"creation_date: {traders[i]['creation_date']}\n"
                f"working: {traders[i]['working']}\n"
                f"initial_deposit: {traders[i]['initial_deposit']}\n"
                f"current_deposit: {traders[i]['current_deposit']}\n"
                f"market: {traders[i]['market']}\n"
                f"exchange: {traders[i]['exchange']}\n"
                f"grid id: {traders[i]['grid']['id']}\n"
                "---------------\n")
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Last {MSG_MAX_SIZE_PC} created traders: \n{data}"
        )
    elif len(command_list) == 2:
        trader_id = command_list[-1]
        trader = requests.get(f"{API_URL}/traders/{trader_id}/").json()
        data = (
            f"id: {trader['id']}\n"
            f"creation_date: {trader['creation_date']}\n"
            f"working: {trader['working']}\n"
            f"initial_deposit: {trader['initial_deposit']}\n"
            f"current_deposit: {trader['current_deposit']}\n"
            f"market: {trader['market']}\n"
            f"exchange: {trader['exchange']}\n"
            f"grid id: {trader['grid']['id']}"
        )
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"{data}"
        )
    elif len(command_list) == 3:
        trader = {
            "exchange": command_list[-2],
            "grid": int(command_list[-1])
        }
        trader_info = requests.post(f"{API_URL}/traders/", data=trader).json()
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Trader created. id: {trader_info['id']}."
        )
    else:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Wrong command. Read the instructions."
        )
