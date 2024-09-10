import os

from dotenv import load_dotenv


load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL")
BYBIT_API_KEY = os.getenv("BYBIT_API_KEY")
BYBIT_SECRET_KEY = os.getenv("BYBIT_SECRET_KEY")
CHECK_TIME_SEC = os.getenv("CHECK_TIME_SEC")
SAFETY_FACTOR = os.getenv("SAFETY_FACTOR")
MINIMUM_ORDER_SIZE = os.getenv("MINIMUM_ORDER_SIZE")
WAITING_TIME_SEC = os.getenv("WAITING_TIME_SEC")

api_requests_mapping = {
    "traders": "/api/traders",
    "deals": "/api/deals",
    "levels": "/api/levels",
    "grids": "/api/grids",
    "tickers": "/api/tickers"
}