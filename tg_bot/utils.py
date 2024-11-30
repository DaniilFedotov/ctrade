import requests

from config import BACKEND_URL, api_requests_mapping


def validate_create_grid_request(command_list):
    """Validates the command to create a grid."""
    try:
        bottom = float(str(command_list[-5]).replace(",", "."))
        top = float(str(command_list[-4]).replace(",", "."))
        number_of_levels = int(command_list[-3])
        deposit = float(str(command_list[-2]).replace(",", "."))
        ticker_id = int(command_list[-1])
        ticker = requests.get(f"{BACKEND_URL}{api_requests_mapping['tickers']}/{ticker_id}/").json()
    except Exception:
        return None, "Create grid error."
    if bottom >= top:
        return None, "The top value cannot be less than the bottom value."
    if number_of_levels % 2 != 0:
        return None, "The number of levels must be even."
    if number_of_levels < 6 or number_of_levels > 40:
        return None, "The number of levels must be more than 6 and less than 40."
    if "Not found." in ticker.values():
        return None, "Ticker does not exist."
    return {
        "bottom": bottom,
        "top": top,
        "number_of_levels": number_of_levels,
        "deposit": deposit,
        "ticker": ticker_id
    }, None
