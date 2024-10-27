import os

from dotenv import load_dotenv


load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL")
BYBIT_API_KEY = os.getenv("BYBIT_API_KEY")
BYBIT_RECV_WINDOW = int(os.getenv("BYBIT_RECV_WINDOW"))
BYBIT_SECRET_KEY = os.getenv("BYBIT_SECRET_KEY")
CHECK_TIME_SEC = float(os.getenv("CHECK_TIME_SEC"))
SAFETY_FACTOR = float(os.getenv("SAFETY_FACTOR"))
MINIMAL_CHECK_TIME_SEC = float(os.getenv("MINIMAL_CHECK_TIME_SEC"))
MINIMUM_ORDER_SIZE = float(os.getenv("MINIMUM_ORDER_SIZE"))
WAITING_TIME_SEC = float(os.getenv("WAITING_TIME_SEC"))

api_requests_mapping = {
    "traders": "/api/traders",
    "deals": "/api/deals",
    "levels": "/api/levels",
    "grids": "/api/grids",
    "tickers": "/api/tickers"
}
