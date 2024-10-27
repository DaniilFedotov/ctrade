import logging
import time

from config import CHECK_TIME_SEC, MINIMAL_CHECK_TIME_SEC
from core.classes import TradingBot
from core.managers import DealManager, GridManager, LevelManager, TraderManager
from strategy.grid_trading.utils import install_grid, update_state, remove_grid


logger = logging.getLogger(__name__)


def check_orders(trader: dict, trading_bot: TradingBot):
    """Checks orders statuses."""
    logger.debug("Start checking orders")
    cur_grid = trader["grid"]
    cur_levels = trader["grid"]["levels"]
    orders_info = trading_bot.get_open_orders()
    logger.debug(f"orders_info: {orders_info}")
    for level in cur_levels:
        order_status = None
        for ind, order in enumerate(orders_info):
            if level["order_id"] == order["orderId"]:
                order_status = order["orderStatus"]
                orders_info.pop(ind)
                break
        logger.debug(f"Order id: {level['order_id']}"
                     f"Order status: {order_status}")
        if order_status == "New":
            continue
        elif order_status is None:
            order_info = trading_bot.get_order(
                order_id=level["order_id"],
                closed=True
            )
            logger.debug(f"Order info: {order_info}")
            if order_info:
                order_status = order_info[0]["orderStatus"]
                if order_status == "Filled":
                    logger.debug("Find filled order")
                    if level["inverse"]:
                        logger.debug("Deal editing")
                        DealManager.update_deal(
                            deal_id=level["deal"],
                            deal_data={"exit_price": level["price"]}
                        )
                        level["deal"] = ""
                    else:
                        logger.debug("Deal creating")
                        ticker_id = trading_bot.grid["ticker"]["id"]
                        deal = DealManager.create_deal(
                            deal_data={
                                "ticker": ticker_id,
                                "side": ("long"
                                         if level["side"] == "buy"
                                         else "short"),
                                "quantity": level["quantity"],
                                "entry_price": level["price"],
                                "trader": trading_bot.trader_id
                            }
                        )
                        logger.debug(f"Deal: {deal}")
                        level["deal"] = deal["id"]
                    next_price = trading_bot.trading_pair.value_formatting(
                        value=(level["price"] - cur_grid["step"]
                               if level["side"] == "sell"
                               else level["price"] + cur_grid["step"]),
                        parameter="price"
                    )
                    next_quantity = trading_bot.trading_pair.value_formatting(
                        value=(cur_grid["order_size"] / next_price
                               if level["inverse"]
                               else level["quantity"]),
                        parameter="quantity"
                    )
                    next_level = {
                        "side": "buy" if level["side"] == "sell" else "sell",
                        "order_id": None,
                        "price": next_price,
                        "quantity": next_quantity,
                        "inverse": not level["inverse"],
                        "deal": level["deal"]
                    }
                    order_id = trading_bot.create_limit_order(
                        side=next_level["side"],
                        quantity=next_level["quantity"],
                        price=next_level["price"]
                    )
                    logger.debug(f"Order id: {order_id}")
                    LevelManager.update_level(
                        level_id=level["id"],
                        level_data=next_level
                    )
                    logger.debug(f"Next level: {next_level}")
                    trading_bot = update_state(trading_bot)
            else:
                order_info = trading_bot.get_order(
                    order_id=level["order_id"],
                )
                if order_info:
                    order_status = order_info[0]["orderStatus"]
                    if order_status == "New":
                        continue
                logger.debug("Order not found")
                continue


def trading_process(trading_bot: TradingBot):
    """Main trading function."""
    logger.debug("Start trading")
    trader = TraderManager.get_trader(
        trader_id=trading_bot.trader_id
    )
    logger.debug(f"Trader: {trader}")
    if not trader["initial_deposit"]:
        logger.debug("Get initial_deposit")
        balance = trading_bot.get_balance()
        TraderManager.update_trader(
            trader_id=trading_bot.trader_id,
            trader_data={
                "initial_deposit": balance,
                "current_deposit": balance
            }
        )
    while trader["working"]:

        cur_price = trading_bot.trading_pair.value_formatting(
            value=trading_bot.check_price(),
            parameter="price"
        )

        if trader["grid"]["bottom"] <= cur_price <= trader["grid"]["top"]:
            if not trader["grid"]["installed"]:
                install_grid(trading_bot)
            check_orders(
                trader=trader,
                trading_bot=trading_bot
            )
            time.sleep(CHECK_TIME_SEC)
        else:
            if trader["grid"]["installed"]:
                remove_grid(trading_bot)
            time.sleep(MINIMAL_CHECK_TIME_SEC)

        trader = TraderManager.get_trader(
            trader_id=trading_bot.trader_id
        )
        logger.debug(f"Trader: {trader}")
