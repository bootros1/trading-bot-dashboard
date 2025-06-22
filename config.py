ACCOUNT_LOGIN = 93863590  # Replace with your MT5 account login
ACCOUNT_PASSWORD = 'H@6eBsBb'  # Replace with your MT5 account password
SERVER = 'MetaQuotes-Demo'  # Replace with your broker's server

# --- List of symbols to be scanned by the bot ---
# Use the scan_symbols.py script to generate this list based on your criteria.
# Or manually edit the list below.
SYMBOLS = ["EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "USDCAD"]

# --- Timeframe ---
# Use MetaTrader 5 timeframes, e.g., 'M15', 'H1', 'D1', etc.
TIMEFRAME = 'M15'

# --- Lot Sizing & Risk ---
# This is the master switch for lot sizing method.
# If True, the bot uses a fixed lot size defined by LOT_SIZE.
# If False, the bot uses a dynamic lot size based on RISK_PER_TRADE.
USE_FIXED_LOT_SIZE = False
LOT_SIZE = 0.01  # Used only if USE_FIXED_LOT_SIZE is True
RISK_PER_TRADE = 0.01  # Risk 1% of account balance per trade. Used if USE_FIXED_LOT_SIZE is False.

# --- ATR-Based Stop-Loss and Take-Profit ---
ATR_PERIOD = 14  # Period for ATR calculation
ATR_SL_MULTIPLIER = 2.0  # Stop-loss will be set at X times the ATR value
REWARD_RISK_RATIO = 1.5  # Take-profit will be X times the stop-loss distance

# --- Backtest Settings ---
# Set to True to run a backtest using historical data.
# Set to False for live trading.
BACKTEST = False
INITIAL_BALANCE = 10000  # Starting balance for the backtest

# --- Logging ---
LOG_DIR = 'logs/'

# --- Telegram Notifications ---
# Replace with your Telegram Bot Token and Chat ID
TELEGRAM_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN' # <-- IMPORTANT: Replace with your real token
TELEGRAM_CHAT_ID = 'YOUR_TELEGRAM_CHAT_ID' # <-- IMPORTANT: Replace with your real chat ID

# NOTE: Pip value is currently hardcoded for major pairs.
# A more advanced version would calculate this dynamically based on the symbol.
