import logging
import time

from config import MINIMUM_ORDER_SIZE, SAFETY_FACTOR, WAITING_TIME_SEC
from core.classes import TradingBot
from core.managers import DealManager, GridManager, LevelManager, TraderManager


logger = logging.getLogger(__name__)


def install_grid(trading_bot: TradingBot):
    """Places trading grid orders."""
    logger.debug("Install grid")
    reset_progress(trading_bot=trading_bot)

    grid = trading_bot.grid
    logger.debug(f"Grid: {grid}")
    if grid["number_of_levels"] % 2 != 0:
        logger.debug("Not even number of levels")
        return False  # raise custom_exception
    balance = trading_bot.get_balance()
    TraderManager.update_trader(
        trader_id=trading_bot.trader_id,
        trader_data={"lock": balance - grid["deposit"]}
    )
    step = trading_bot.trading_pair.value_formatting(
        value=((grid["top"] - grid["bottom"]) / (grid["number_of_levels"] - 1)),
        parameter="price"
    )
    order_size = trading_bot.trading_pair.value_formatting(
        value=grid["deposit"] / grid["number_of_levels"],
        parameter="price"
    )
    GridManager.update_grid(
        grid_id=grid["id"],
        grid_data={"step": step, "order_size": order_size}
    )
    middle = trading_bot.trading_pair.value_formatting(
        value=(grid["top"] + grid["bottom"]) / 2,
        parameter="price"
    )
    cur_price = trading_bot.trading_pair.value_formatting(
        value=trading_bot.check_price(),
        parameter="price"
    )
    logger.debug(f"Current price: {cur_price}"
                 f"Balance: {balance}"
                 f"Step: {step}"
                 f"Order size: {order_size}"
                 f"Middle: {middle}")

    levels = []
    for ind in range(int(grid["number_of_levels"] / 2)):
        init_top_price = middle + (0.5 + ind) * step
        init_bottom_price = middle - (0.5 + ind) * step
        right_pos_top = init_top_price >= cur_price
        right_pos_bottom = init_bottom_price < cur_price

        top_price = trading_bot.trading_pair.value_formatting(
            value=init_top_price if right_pos_top else init_top_price - step,
            parameter="price"
        )
        bottom_price = trading_bot.trading_pair.value_formatting(
            value=init_bottom_price if right_pos_bottom else init_bottom_price + step,
            parameter="price"
        )

        top_qty = trading_bot.trading_pair.value_formatting(
            value=order_size / top_price,
            parameter="quantity"
        )
        bottom_qty = trading_bot.trading_pair.value_formatting(
            value=order_size / bottom_price,
            parameter="quantity"
        )

        logger.debug(f"Index: {ind}\n"
                     f"Initial top price: {init_top_price}, initial bottom price: {init_bottom_price}\n"
                     f"Right position top: {right_pos_top}, right position bottomL {right_pos_bottom}\n"
                     f"Top price: {top_price}, bottom price: {bottom_price}\n"
                     f"Top quantity: {top_qty}, bottom quantity: {bottom_qty}")

        top_level = {
            "side": "sell" if right_pos_top else "buy",
            "order_id": None,
            "price": top_price,
            "quantity": top_qty,
            "inverse": False if right_pos_top else True,
            "grid": grid["id"],
            "deal": ""
        }
        bottom_level = {
            "side": 'buy' if right_pos_bottom else "sell",
            "order_id": None,
            "price": bottom_price,
            "quantity": bottom_qty,
            "inverse": False if right_pos_bottom else True,
            "grid": grid["id"],
            "deal": ""
        }
        levels.append(top_level)
        levels.append(bottom_level)
    logger.debug(f"Levels: {levels}")
    required_token_balance = 0
    for level in levels:
        if level["side"] == "sell":
            required_token_balance += level["quantity"]
        if level["inverse"]:
            ticker = grid["ticker"]["id"]
            entry_price = trading_bot.trading_pair.value_formatting(
                value=level["price"] - step if level["side"] == "sell" else level["price"] + step,
                parameter="price"
            )
            side = "long" if level["side"] == "sell" else "short"
            deal = {
                "ticker": ticker,
                "side": side,
                "quantity": level["quantity"],
                "entry_price": entry_price,
                "trader": trading_bot.trader_id
            }
            deal_info = DealManager.create_deal(
                deal_data=deal
            )
            logger.debug(f"Deal info: {deal_info}")
            level["deal"] = deal_info["id"]

    token_balance = trading_bot.get_balance(coin=trading_bot.trading_pair.token)
    logger.debug(f"Token balance: {token_balance}")
    if token_balance < required_token_balance:
        required_qty = trading_bot.trading_pair.value_formatting(
            value=(required_token_balance - token_balance) * SAFETY_FACTOR,
            parameter="quantity"
        )
        logger.debug(f"Not enough tokens. Required quantity: {required_qty}")
        trading_bot.create_market_order(
            side="buy",
            quantity=required_qty,
            market_unit="baseCoin"
        )
    elif token_balance > required_token_balance:
        excess_qty = trading_bot.trading_pair.value_formatting(
            value=token_balance - required_token_balance,
            parameter="quantity"
        )
        logger.debug(f"Excess tokens. Excess quantity: {excess_qty}")
        cur_price = trading_bot.trading_pair.value_formatting(
            value=trading_bot.check_price(),
            parameter="price"
        )
        if excess_qty * cur_price >= MINIMUM_ORDER_SIZE:
            logger.debug(f"Create market order")
            trading_bot.create_market_order(
                side="sell",
                quantity=excess_qty,
                market_unit="baseCoin"
            )
    else:
        pass

    for level in levels:
        order_id = trading_bot.create_limit_order(
            side=level["side"],
            quantity=level["quantity"],
            price=level["price"]
        )
        logger.debug(f"Order id: {order_id}")
        level["order_id"] = order_id
        LevelManager.create_level(
            level_data=level
        )
    GridManager.update_grid(
        grid_id=grid["id"],
        grid_data={"installed": True}
    )
    logger.debug("Grid installed")
    return True


def finish_trading(trading_bot: TradingBot):
    """Close the trade."""
    logger.debug("Finish trading")
    reset_progress(trading_bot=trading_bot)
    token_balance = trading_bot.trading_pair.value_formatting(
        value=trading_bot.get_balance(trading_bot.trading_pair.token),
        parameter="quantity"
    )
    cur_price = trading_bot.trading_pair.value_formatting(
        value=trading_bot.check_price(),
        parameter="price"
    )
    logger.debug(f"Token balance: {token_balance}"
                 f"Current price: {cur_price}")
    if token_balance * cur_price < MINIMUM_ORDER_SIZE:
        trading_bot.create_market_order(
            side="sell",
            quantity=token_balance,
            market_unit="baseCoin"
        )
    GridManager.update_grid(
        grid_id=trading_bot.grid["id"],
        grid_data={"installed": False}
    )


def reset_progress(trading_bot: TradingBot):
    """Resets levels and opened orders."""
    logger.debug("Reset progress")
    trading_bot.cancel_all_orders()
    trader = TraderManager.get_trader(
        trader_id=trading_bot.trader_id
    )
    for level in trader["grid"]["levels"]:
        LevelManager.delete_level(
            level_id=str(level["id"])
        )
    time.sleep(WAITING_TIME_SEC)


def update_state(trading_bot: TradingBot):
    """Updates state for trader and grid."""
    logger.debug("Update state")
    balance = trading_bot.get_balance()
    TraderManager.update_trader(
        trader_id=trading_bot.trader_id,
        trader_data={"current_deposit": balance}
    )
    trader = TraderManager.get_trader(
        trader_id=trading_bot.trader_id
    )
    grid_deposit = balance - trader["lock"]
    order_size = trading_bot.trading_pair.value_formatting(
        value=grid_deposit / trading_bot.grid["number_of_levels"],
        parameter="price"
    )
    GridManager.update_grid(
        grid_id=trading_bot.grid["id"],
        grid_data={"deposit": grid_deposit, "order_size": order_size}
    )
    trading_bot.grid = GridManager.get_grid(
        grid_id=trading_bot.grid["id"]
    )
    logger.debug(f"Balance: {balance}"
                 f"Trader: {trader}"
                 f"Grid deposit: {grid_deposit}"
                 f"Order size: {order_size}"
                 f"Grid: {trading_bot.grid}")
    return trading_bot
