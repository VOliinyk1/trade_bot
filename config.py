import os
from dotenv import load_dotenv

load_dotenv()

# Binance API
BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET")

# OpenAI API
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Telegram Bot
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")

# Trading Configuration
TRADING_PAIRS = os.getenv("TRADING_PAIRS", "BTCUSDT,ETHUSDT,BNBUSDT,ADAUSDT,SOLUSDT").split(",")
ANALYSIS_INTERVAL = int(os.getenv("ANALYSIS_INTERVAL", "300"))  # 5 хвилин
SIGNAL_THRESHOLD = float(os.getenv("SIGNAL_THRESHOLD", "0.7"))

# News Sources
NEWS_SOURCES = os.getenv("NEWS_SOURCES", "coindesk,cointelegraph,decrypt").split(",")
NEWS_UPDATE_INTERVAL = int(os.getenv("NEWS_UPDATE_INTERVAL", "600"))  # 10 хвилин

# Technical Analysis Settings
RSI_PERIOD = 14
MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9
EMA_PERIOD = 20
BB_PERIOD = 20
BB_STD = 2

# Risk Management
MAX_POSITION_SIZE_USDT = 1000
STOP_LOSS_PERCENT = 5
TAKE_PROFIT_PERCENT = 10
