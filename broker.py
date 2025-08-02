import MetaTrader5 as mt5
from config import ACCOUNT_LOGIN, ACCOUNT_PASSWORD, SERVER
from utils import setup_logger
from notifier import send_telegram

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

    symbol_info = mt5.symbol_info(symbol)
    if symbol_info is None:
        logger.error(f"Symbol info not found for {symbol}")
        return False

    # Debug: Log all symbol info and supported filling mode
    logger.info(f"Symbol info for {symbol}: {symbol_info}")
    logger.info(f"Supported filling mode for {symbol}: {symbol_info.filling_mode}")

    # Try all common filling modes
    filling_modes = [mt5.ORDER_FILLING_FOK, mt5.ORDER_FILLING_IOC, mt5.ORDER_FILLING_RETURN]
    for filling_mode in filling_modes:
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
            "type_filling": filling_mode,
        }
        result = mt5.order_send(request)
        if result.retcode == mt5.TRADE_RETCODE_DONE:
            logger.info(f"Order placed: {direction} {lot} lots at {price} with filling mode {filling_mode}")
            send_telegram(
                f"✅ Trade executed:\nSymbol: {symbol}\nDirection: {direction}\nLot: {lot}\nEntry: {price:.5f}\nSL: {sl:.5f}\nTP: {tp:.5f}\nFilling Mode: {filling_mode}"
            )
            return True
        else:
            logger.warning(f"Order failed with filling mode {filling_mode}: {result.comment}")
    logger.error(f"Order failed for all filling modes for {symbol}")
    send_telegram(
        f"❌ Trade FAILED:\nSymbol: {symbol}\nDirection: {direction}\nLot: {lot}\nEntry: {price:.5f}\nSL: {sl:.5f}\nTP: {tp:.5f}\nError: All filling modes failed."
    )
    return False
# NOTE: Pip value is hardcoded for EURUSD ($10 per lot per pip). For other symbols, adjust risk.py accordingly. 