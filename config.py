import os

# Broker Selection
BROKER = "KRAKEN"  # "OANDA" or "KRAKEN"

# OANDA Configuration (Demo Environment)
OANDA_API_KEY = os.getenv("OANDA_API_KEY", 'ced9a1579c290683dc1cbe4431b9a56a-58a4a53964cf95837b3c6d6e67d6759d')
OANDA_ACCOUNT_ID = os.getenv("OANDA_ACCOUNT_ID", '101-001-10517453-001')
OANDA_ENVIRONMENT = os.getenv("OANDA_ENVIRONMENT", 'practice')  # 'practice' for demo, 'live' for live trading
OANDA_BASE_URL = os.getenv("OANDA_BASE_URL", 'https://api-fxpractice.oanda.com')  # Demo environment

# Kraken Configuration
KRAKEN_API_KEY = os.getenv("KRAKEN_API_KEY", 'rpYXJ8I6w0iIfi/0LSjkGt/hX9gYh0MxFNJBgM1W2vVzl/tF62QClOSf')
KRAKEN_API_SECRET = os.getenv("KRAKEN_API_SECRET", '/ZA2OLReFy1PkZ9HPUzfVXab+Ju5kGQu4jAjaQ7PclVbOI1LNrqgVcw5Vpn22C2e0lP9C2ay+qLmRZoHxlc6cw==')
KRAKEN_SANDBOX = os.getenv("KRAKEN_SANDBOX", "False").lower() == "true"  # Kraken doesn't support sandbox in CCXT

# Legacy MT5 Configuration (for reference)
ACCOUNT_LOGIN = os.getenv("MT5_ACCOUNT_LOGIN", "93863590")
ACCOUNT_PASSWORD = os.getenv("MT5_ACCOUNT_PASSWORD", "H@6eBsBb")
SERVER = os.getenv("MT5_SERVER", "MetaQuotes-Demo")

# --- List of symbols to be scanned by the bot ---
# OANDA uses different symbol format: EUR_USD, GBP_USD, etc.
# Kraken uses different symbol format: BTC/USD, ETH/USD, etc.
OANDA_SYMBOLS = ["EUR_USD", "GBP_USD", "USD_JPY", "AUD_USD", "USD_CAD"]
KRAKEN_SYMBOLS = [
    "BTC/USD", "ETH/USD", "XRP/USD", "ADA/USD", "DOT/USD",
    "LTC/USD", "BCH/USD", "LINK/USD", "UNI/USD", "SOL/USD",
    "AVAX/USD", "ATOM/USD", "NEAR/USD", "1INCH/USD", "AAVE/USD",
    "ALGO/USD", "ALICE/USD", "APT/USD", "ARB/USD", "AXS/USD"
]

# --- Timeframe ---
# OANDA uses different timeframe format: M15, H1, D, etc.
# Kraken uses CCXT format: 15m, 1h, 1d, etc.
TIMEFRAME = os.getenv("TIMEFRAME", 'M15')

# --- Lot Sizing & Risk ---
USE_FIXED_LOT_SIZE = os.getenv("USE_FIXED_LOT_SIZE", "False").lower() == "true"
LOT_SIZE = float(os.getenv("LOT_SIZE", "0.01"))  # Used only if USE_FIXED_LOT_SIZE is True
RISK_PER_TRADE = float(os.getenv("RISK_PER_TRADE", "0.01"))  # Risk 1% of account balance per trade
TRADE_PERCENTAGE = float(os.getenv("TRADE_PERCENTAGE", "0.25"))  # 25% of balance per trade

# --- ATR-Based Stop-Loss and Take-Profit ---
ATR_PERIOD = int(os.getenv("ATR_PERIOD", "14"))  # Period for ATR calculation
ATR_SL_MULTIPLIER = float(os.getenv("ATR_SL_MULTIPLIER", "2.0"))  # Stop-loss will be set at X times the ATR value
REWARD_RISK_RATIO = float(os.getenv("REWARD_RISK_RATIO", "1.5"))  # Take-profit will be X times the stop-loss distance

# --- Backtest Settings ---
BACKTEST = os.getenv("BACKTEST", "False").lower() == "true"
INITIAL_BALANCE = float(os.getenv("INITIAL_BALANCE", "10000"))

# --- Logging ---
LOG_DIR = os.getenv("LOG_DIR", 'logs/')

# --- Telegram Notifications ---
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", '7824709521:AAF1LU4t2p9Q4PgeGU0gmTOAh_mg9rfNStU')
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", '1863761788')

def get_symbols():
    """Get symbols based on selected broker."""
    if BROKER.upper() == "OANDA":
        return OANDA_SYMBOLS
    elif BROKER.upper() == "KRAKEN":
        return KRAKEN_SYMBOLS
    else:
        return OANDA_SYMBOLS  # Default to OANDA symbols
