import MetaTrader5 as mt5
import pandas as pd
import time
import platform
import os
from config import ACCOUNT_LOGIN, ACCOUNT_PASSWORD, SERVER

# User settings
SYMBOLS = ['EURUSD', 'GBPUSD', 'USDJPY']  # Add more symbols as needed
TIMEFRAMES = ['M15', 'H1']  # Add more timeframes as needed
BARS = 500  # Number of bars to fetch
INTERVAL_MINUTES = 0  # Set >0 to run in a loop every N minutes, or 0 for one-time fetch

# Path to MT5 terminal (update if your MT5 is installed elsewhere)
MT5_PATHS = [
    r"C:\Program Files\MetaTrader 5\terminal64.exe",
    r"C:\Program Files\MetaTrader 5\terminal.exe",
    r"C:\Program Files (x86)\MetaTrader 5\terminal64.exe",
    r"C:\Program Files (x86)\MetaTrader 5\terminal.exe"
]

def print_diagnostics():
    print("Python architecture:", platform.architecture())
    print("MT5 package path:", mt5.__file__)
    print("Current working directory:", os.getcwd())
    print("MetaTrader5 version:", mt5.version())

def try_initialize():
    print("Trying mt5.initialize() with no arguments...")
    if mt5.initialize():
        print("Connected to running terminal (no credentials).")
        return True
    print("Failed. Error:", mt5.last_error())
    print("Trying mt5.initialize() with credentials...")
    if mt5.initialize(login=ACCOUNT_LOGIN, password=ACCOUNT_PASSWORD, server=SERVER):
        print("Connected using credentials.")
        return True
    print("Failed. Error:", mt5.last_error())
    for path in MT5_PATHS:
        print(f"Trying mt5.initialize(path='{path}') with credentials...")
        if mt5.initialize(path=path, login=ACCOUNT_LOGIN, password=ACCOUNT_PASSWORD, server=SERVER):
            print(f"Connected using credentials and path: {path}")
            return True
        print("Failed. Error:", mt5.last_error())
    return False

def _get_mt5_timeframe(timeframe_str):
    try:
        return getattr(mt5, f'TIMEFRAME_{timeframe_str}')
    except AttributeError:
        print(f"Invalid timeframe: {timeframe_str}")
        return None

def fetch_and_save(symbol, timeframe_str):
    timeframe = _get_mt5_timeframe(timeframe_str)
    if timeframe is None:
        return
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, BARS)
    if rates is None or len(rates) == 0:
        print(f"No data fetched for {symbol} {timeframe_str}.")
        return
    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    df = df[['time','open','high','low','close','tick_volume','spread','real_volume']]
    filename = f"historical_{symbol}_{timeframe_str}.csv"
    df.to_csv(filename, index=False)
    print(f"Saved {len(df)} bars to {filename}")

def run_fetch():
    print_diagnostics()
    if not try_initialize():
        print("\nERROR: Could not connect to MetaTrader 5 terminal. Please check your installation, credentials, and terminal path.")
        return
    print("\nAccount info:", mt5.account_info())
    print("Symbols in Market Watch:", [s.name for s in mt5.symbols_get()])
    for symbol in SYMBOLS:
        for tf in TIMEFRAMES:
            fetch_and_save(symbol, tf)
    mt5.shutdown()

def main():
    if INTERVAL_MINUTES > 0:
        print(f"Running in loop every {INTERVAL_MINUTES} minutes. Press Ctrl+C to stop.")
        try:
            while True:
                run_fetch()
                print(f"Sleeping for {INTERVAL_MINUTES} minutes...")
                time.sleep(INTERVAL_MINUTES * 60)
        except KeyboardInterrupt:
            print("Stopped by user.")
    else:
        run_fetch()

if __name__ == '__main__':
    main() 