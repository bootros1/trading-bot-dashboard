import MetaTrader5 as mt5
from config import ACCOUNT_LOGIN, ACCOUNT_PASSWORD, SERVER
from utils import setup_logger

logger = setup_logger('broker')

def _get_mt5_timeframe(timeframe_str):
    # Converts string like 'M15' to mt5.TIMEFRAME_M15
    try:
        return getattr(mt5, f'TIMEFRAME_{timeframe_str}')
    except AttributeError:
        logger.error(f"Invalid timeframe: {timeframe_str}")
        return None

def connect():
    if not mt5.initialize(server=SERVER, login=ACCOUNT_LOGIN, password=ACCOUNT_PASSWORD):
        logger.error(f"MT5 initialize() failed, error code: {mt5.last_error()}")
        return False
    logger.info("Connected to MetaTrader 5")
    return True

def disconnect():
    mt5.shutdown()
    logger.info("Disconnected from MetaTrader 5")

def get_account_info():
    info = mt5.account_info()
    if info is None:
        logger.error("Failed to get account info")
        return None
    return info

def get_historical_data(symbol, timeframe, bars=100):
    mt5_timeframe = _get_mt5_timeframe(timeframe)
    if mt5_timeframe is None:
        return None
    rates = mt5.copy_rates_from_pos(symbol, mt5_timeframe, 0, bars)
    import pandas as pd
    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    return df

def place_order(symbol, direction, lot, sl, tp):
    price = mt5.symbol_info_tick(symbol).ask if direction == 'buy' else mt5.symbol_info_tick(symbol).bid
    order_type = mt5.ORDER_TYPE_BUY if direction == 'buy' else mt5.ORDER_TYPE_SELL
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": order_type,
        "price": price,
        "sl": sl,
        "tp": tp,
        "deviation": 10,
        "magic": 234000,
        "comment": "AI Forex Bot",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    result = mt5.order_send(request)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        logger.error(f"Order failed: {result.comment}")
        return False
    logger.info(f"Order placed: {direction} {lot} lots at {price}")
    return True
# NOTE: Pip value is hardcoded for EURUSD ($10 per lot per pip). For other symbols, adjust risk.py accordingly. 