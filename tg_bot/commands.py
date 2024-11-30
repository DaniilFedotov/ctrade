import datetime

import requests

from config import AVAILABLE_EXCHANGES, BACKEND_URL, MSG_MAX_SIZE_PC, api_requests_mapping
from utils import validate_create_grid_request


def start_trading(update, context):
    """Launches the specified bot."""
    command = update["message"]["text"].split(" ")
    if len(command) == 2:
        bot_id = int(command[1])
        trader = requests.get(
            f"{BACKEND_URL}{api_requests_mapping['traders']}/{bot_id}/"
        ).json()
        if "Not found." in trader.values():
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Trader does not exist."
            )
            return
        if trader["working"]:
            text="This bot is already running."
        else:
            response = requests.patch(
                f"{BACKEND_URL}{api_requests_mapping['traders']}/{bot_id}/",
                data={"working": True}
            )
            if response.status_code == 200:
                text=f"The bot {bot_id} is running."
            else:
                text = "Unexpected error."
    else:
        text = "Bot number not specified."

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text
    )


def stop_trading(update, context):
    """Stops the specified bot."""
    command = update["message"]["text"].split(" ")
    if len(command) == 2:
        bot_id = int(command[1])
        trader = requests.get(
            f"{BACKEND_URL}{api_requests_mapping['traders']}/{bot_id}/"
        ).json()
        if "Not found." in trader.values():
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Trader does not exist."
            )
            return
        if trader["working"]:
            response = requests.patch(
                f"{BACKEND_URL}{api_requests_mapping['traders']}/{bot_id}/",
                data={"working": False}
            )
            if response.status_code == 200:
                text=f"The bot {bot_id} is stopped."
            else:
                text="Unexpected error."
        else:
            text="This bot has already been stopped."
    else:
        text="Bot number not specified."

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text
    )


def get_revenue(update, context):
    """Calculates revenue for recent transactions."""
    command = update["message"]["text"].split(" ")
    if len(command) == 2:
        num_of_deals = int(command[1])
    else:
        num_of_deals = 5
    deals = requests.get(f"{BACKEND_URL}{api_requests_mapping['deals']}/").json()
    if len(deals) < num_of_deals:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="The requested number of deals is greater than number of closed deals."
        )
        num_of_deals = len(deals)
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
    deals = requests.get(f"{BACKEND_URL}{api_requests_mapping['deals']}/").json()
    today = datetime.datetime.today()
    day = "today" if update["message"]["text"] == "/daily" else "yesterday"
    day_date = (today if day == "today" else today - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    revenue = 0
    for deal in deals:
        if deal["opening_date"] == day_date and deal["closed"]:
            revenue += deal["revenue"]
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Revenue for {day}: {revenue} USD."
    )


def get_bot_id(update, context):
    """Give the id of a running trading bot."""
    traders = requests.get(f"{BACKEND_URL}{api_requests_mapping['traders']}/").json()
    bot_id = None
    for trader in traders:
        if trader["working"]:
            bot_id = trader["id"]
            break
    text = f"Id of a running trading bot: {bot_id}." if bot_id else "No running bots found."
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text
    )


def get_tickers(update, context):
    """Displays a list of available tickers."""
    tickers = requests.get(f"{BACKEND_URL}{api_requests_mapping['tickers']}/").json()
    if not tickers:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="The tickers do not exist."
        )
        return
    names = ""
    for ticker in tickers:
        names += f"id: {ticker['id']} name: {ticker['name']}\n"
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Available tickers:\n{names}"
    )


def get_or_create_grids(update, context):
    """Displays a list of available grids or create a new one."""
    command_list = update["message"]["text"].split(" ")
    if len(command_list) == 1:
        grids = requests.get(f"{BACKEND_URL}{api_requests_mapping['grids']}/").json()
        if not grids:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="The grids do not exist."
            )
            return
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
        text = f"Last {MSG_MAX_SIZE_PC} created grids: \n{data}"
    elif len(command_list) == 2:
        grid_id = command_list[-1]
        grid = requests.get(f"{BACKEND_URL}{api_requests_mapping['grids']}/{grid_id}/").json()
        if "Not found." in grid.values():
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Grid does not exist."
            )
            return
        data = (
            f"id: {grid['id']}\n"
            f"bottom: {grid['bottom']}\n"
            f"top: {grid['top']}\n"
            f"number_of_levels: {grid['number_of_levels']}\n"
            f"deposit: {grid['deposit']}\n"
            f"ticker: {grid['ticker']['name']}"
        )
        text = f"{data}"
    elif len(command_list) == 6:
        grid, validation_error_text = validate_create_grid_request(command_list)
        if validation_error_text:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=validation_error_text
            )
            return
        grid_info = requests.post(f"{BACKEND_URL}{api_requests_mapping['grids']}/", data=grid).json()
        if "id" in grid_info:
            text = f"Grid created. id: {grid_info['id']}."
        else:
            text = "Create grid error."
    else:
        text = "Wrong command. Read the instructions."
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text
    )


def get_or_create_traders(update, context):
    """Displays a list of available traders or create a new one."""
    command_list = update["message"]["text"].split(" ")
    if len(command_list) == 1:
        traders = requests.get(f"{BACKEND_URL}{api_requests_mapping['traders']}/").json()
        if not traders:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="The traders do not exist."
            )
            return
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
        text = f"Last {MSG_MAX_SIZE_PC} created traders: \n{data}"
    elif len(command_list) == 2:
        trader_id = command_list[-1]
        trader = requests.get(f"{BACKEND_URL}{api_requests_mapping['traders']}/{trader_id}/").json()
        if "Not found." in trader.values():
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Trader does not exist."
            )
            return
        text = (
            f"id: {trader['id']}\n"
            f"creation_date: {trader['creation_date']}\n"
            f"working: {trader['working']}\n"
            f"initial_deposit: {trader['initial_deposit']}\n"
            f"current_deposit: {trader['current_deposit']}\n"
            f"market: {trader['market']}\n"
            f"exchange: {trader['exchange']}\n"
            f"grid id: {trader['grid']['id']}"
        )
    elif len(command_list) == 3:
        exchange = command_list[-2]
        grid_id = int(command_list[-1])
        if exchange not in AVAILABLE_EXCHANGES:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="This exchange is not supported."
            )
            return
        grid = requests.get(f"{BACKEND_URL}{api_requests_mapping['grids']}/{grid_id}/").json()
        if "Not found." in grid.values():
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Grid does not exist."
            )
            return
        trader = {
            "exchange": exchange,
            "grid": grid_id
        }
        trader_info = requests.post(f"{BACKEND_URL}{api_requests_mapping['traders']}/", data=trader).json()
        text = f"Trader created. id: {trader_info['id']}."
    else:
        text = "Wrong command. Read the instructions."
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text
    )
