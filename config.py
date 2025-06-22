ACCOUNT_LOGIN = 93863590  # Replace with your MT5 account login
ACCOUNT_PASSWORD = 'H@6eBsBb'  # Replace with your MT5 account password
SERVER = 'MetaQuotes-Demo'  # Replace with your broker's server
# --- List of symbols to be scanned by the bot ---
# Use the scan_symbols.py script to generate this list based on your criteria.
SYMBOLS = ['EURUSD', 'GBPUSD', 'USDJPY', 'AUDUSD', 'USDCAD']

# Use MetaTrader5 timeframes, e.g., 'M15', 'H1', etc. The code will convert this to the MT5 constant.
TIMEFRAME = 'M15'

LOT_SIZE = 0.1 # Default lot size, will be adjusted
RISK_PER_TRADE = 0.01  # 1% risk per trade
TRADE_PERCENTAGE = 0.25  # 25% of balance per trade

# --- ATR-Based Risk Management Settings ---
ATR_PERIOD = 14  # Period for ATR calculation
ATR_SL_MULTIPLIER = 2.0  # Stop-loss will be set at 2 * ATR
REWARD_RISK_RATIO = 1.5  # Take-profit will be 1.5 * the stop-loss distance

LOG_DIR = 'logs/'

# --- Main Settings ---
BACKTEST = True # Set to True to run a backtest, False for live trading

# --- Trading Parameters ---
SYMBOLS = ["EURUSD", "GBPUSD", "USDJPY"] # Symbols to trade or backtest
TIMEFRAME = 'D1' # M1, M5, M15, M30, H1, H4, D1, W1, MN1

# --- Risk Management ---
RISK_PER_TRADE = 0.01 # 1% of account balance
ATR_PERIOD = 14 # Period for ATR calculation
ATR_SL_MULTIPLIER = 2.0 # Stop loss distance in multiples of ATR

# --- Backtest Settings ---
INITIAL_BALANCE = 10000 # Starting balance for the backtest

# --- MT5 Connection ---
ACCOUNT_LOGIN = 93863590
ACCOUNT_PASSWORD = 'H@6eBsBb'
SERVER = 'MetaQuotes-Demo'

# NOTE: Pip value is hardcoded for EURUSD ($10 per lot per 100 pips)
