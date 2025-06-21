import pandas as pd
import numpy as np
from config import ATR_PERIOD

def calculate_rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_ma(series, period=50):
    return series.rolling(window=period).mean()

def calculate_atr(high, low, close, period=14):
    """Calculates the Average True Range (ATR)."""
    tr1 = pd.DataFrame(high - low)
    tr2 = pd.DataFrame(abs(high - close.shift(1)))
    tr3 = pd.DataFrame(abs(low - close.shift(1)))
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    atr = tr.ewm(alpha=1/period, adjust=False).mean()
    return atr

def generate_signal(df):
    """
    Generates a trade signal and the current ATR value.
    Returns a tuple: (signal, atr_value)
    Example: ('buy', 0.0015) or (None, None)
    """
    df = df.copy()  # Avoid SettingWithCopyWarning
    df['rsi'] = calculate_rsi(df['close'])
    df['ma_short'] = calculate_ma(df['close'], period=20)
    df['ma_long'] = calculate_ma(df['close'], period=50)
    df['atr'] = calculate_atr(df['high'], df['low'], df['close'], period=ATR_PERIOD)

    # Ensure we have enough data to calculate indicators
    if df['atr'].isnull().iloc[-1]:
        return None, None
        
    latest = df.iloc[-1]
    prev = df.iloc[-2]
    
    # Buy signal: RSI < 30 and MA20 crosses above MA50
    if latest['rsi'] < 30 and prev['ma_short'] < prev['ma_long'] and latest['ma_short'] > latest['ma_long']:
        return 'buy', latest['atr']
        
    # Sell signal: RSI > 70 and MA20 crosses below MA50
    if latest['rsi'] > 70 and prev['ma_short'] > prev['ma_long'] and latest['ma_short'] < latest['ma_long']:
        return 'sell', latest['atr']
        
    return None, None 