import os

from dotenv import load_dotenv


load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL")
MSG_MAX_SIZE_PC = int(os.getenv("MSG_MAX_SIZE_PC"))
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

AVAILABLE_EXCHANGES = ["binance", "bybit"]

api_requests_mapping = {
    "traders": "/api/traders",
    "deals": "/api/deals",
    "levels": "/api/levels",
    "grids": "/api/grids",
    "tickers": "/api/tickers"
}