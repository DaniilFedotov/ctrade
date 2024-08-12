from exchange.bybit.clients import BybitClient


def get_exchange_client(exchange):
    """Gives the exchange client class for the requested exchange."""
    match exchange:
        case "bybit":
            return BybitClient
