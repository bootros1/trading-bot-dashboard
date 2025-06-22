import pandas as pd
import numpy as np
# Add a check for ATR_PERIOD, if not found, use a default
try:
    from config import ATR_PERIOD
except ImportError:
    ATR_PERIOD = 14

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
    if df['atr'].isnull().iloc[-1] or df['rsi'].isnull().iloc[-1]:
        return None, None
        
    latest = df.iloc[-1]
    
    # --- New Strategy Logic ---
    # Buy signal: MA20 is above MA50 (uptrend) and RSI is oversold.
    if latest['ma_short'] > latest['ma_long'] and latest['rsi'] < 30:
        return 'buy', latest['atr']
        
    # Sell signal: MA20 is below MA50 (downtrend) and RSI is overbought.
    if latest['ma_short'] < latest['ma_long'] and latest['rsi'] > 70:
        return 'sell', latest['atr']
        
    return None, None 