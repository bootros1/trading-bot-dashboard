import os
import sys
import atexit
import signal
from datetime import datetime

# Create a lock file to prevent multiple instances
LOCK_FILE = 'trading_bot.lock'

def create_lock():
    """Create a lock file to prevent multiple instances."""
    if os.path.exists(LOCK_FILE):
        print("Trading bot is already running!")
        sys.exit(1)
    with open(LOCK_FILE, 'w') as f:
        f.write(str(os.getpid()))

def remove_lock():
    """Remove the lock file."""
    if os.path.exists(LOCK_FILE):
        os.remove(LOCK_FILE)

def signal_handler(signum, frame):
    """Handle shutdown signals gracefully."""
    print("\nShutting down trading bot...")
    remove_lock()
    sys.exit(0)

# Set up signal handlers
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

# Create lock file
create_lock()
atexit.register(remove_lock)

try:
    # Import unified trader interface
    from trader_interface import MultiTrader, TraderFactory
    from strategy import generate_signal
    from risk import calculate_units, get_sl_tp
    from utils import setup_logger, log_trade
    from config import BROKER, TIMEFRAME, ATR_SL_MULTIPLIER, BACKTEST, INITIAL_BALANCE, get_symbols
    from backtest import run_backtest
    import pandas as pd
    from datetime import datetime

    logger = setup_logger('main')

    def live_trading():
        """Scans multiple symbols and executes a trade on the first valid signal using unified trader."""
        # Create multi-trader with selected broker
        multi_trader = MultiTrader(primary_broker=BROKER)
        
        # Add the selected broker
        if not multi_trader.add_broker(BROKER):
            logger.error(f"Failed to connect to {BROKER}")
            return

        info = multi_trader.get_account_info()
        if info is None:
            logger.error(f"Failed to get account info from {BROKER}")
            multi_trader.disconnect_all()
            return
        
        balance = info['balance']
        trade_executed = False
        symbols = get_symbols()

        logger.info(f"Scanning {len(symbols)} symbols for a signal using {BROKER}...")

        for symbol in symbols:
            logger.info(f"--- Analyzing {symbol} ---")
            df = multi_trader.get_historical_data(symbol, TIMEFRAME, bars=100)
            if df is None or df.empty:
                logger.warning(f"Could not get historical data for {symbol}. Skipping.")
                continue

            signal, atr = generate_signal(df)
            if signal and atr:
                logger.info(f"Signal FOUND for {symbol}: {signal.upper()}, ATR: {atr:.5f}")
                
                # Convert ATR to pips for position sizing
                pip_size = 0.0001  # For 5-digit brokers
                sl_pips = (atr * ATR_SL_MULTIPLIER) / pip_size

                price = df.iloc[-1]['close']
                # Calculate units instead of lot size for OANDA
                units = calculate_units(balance, sl_pips)
                sl, tp = get_sl_tp(price, signal, atr)
                
                if units > 0 and sl is not None:
                    # For Kraken, use amount directly; for OANDA, convert to lot size
                    if BROKER.upper() == "KRAKEN":
                        amount = units / 100000.0  # Convert to smaller amount for crypto
                    else:
                        amount = units / 100000.0  # Convert to lot size for OANDA
                    
                    success = multi_trader.place_order(symbol, signal, amount, sl, tp)
                    if success:
                        logger.info(f"Trade executed for {symbol}: {signal} {units} units at {price}, SL: {sl:.5f}, TP: {tp:.5f}")
                        trade_executed = True
                        trade_data = {
                            'timestamp': datetime.now().isoformat(),
                            'symbol': symbol,
                            'direction': signal,
                            'units': units,
                            'entry': price,
                            'sl': sl,
                            'tp': tp,
                            'result': 'executed',
                            'error': '',
                            'pnl': 0,  # Placeholder for now
                            'balance': balance,
                            'broker': BROKER
                        }
                        log_trade(trade_data)
                        break  # Stop scanning after one successful trade
                    else:
                        logger.error(f"Failed to place order for {symbol}. Will continue scanning.")
                else:
                    logger.warning(f"Could not calculate valid units or SL/TP for {symbol}. Skipping trade.")
            else:
                logger.info(f"No signal for {symbol}.")

        if not trade_executed:
            logger.info("Scan complete. No valid trading signals found on any symbol today.")

        multi_trader.disconnect_all()

    def main():
        """Main function to run the trading bot."""
        logger.info(f"Starting {BROKER} Trading Bot...")
        
        if BACKTEST:
            logger.info("Running in backtest mode...")
            # For backtesting, you'll need to adapt the data format
            # This is a placeholder - you may need to modify backtest.py for multi-broker
            import pandas as pd
            try:
                df = pd.read_csv('historical_data.csv')
                results = run_backtest(df)
                results.to_csv('logs/backtest_results.csv', index=False)
                logger.info("Backtest completed successfully")
            except Exception as e:
                logger.error(f"Backtest failed: {e}")
        else:
            logger.info(f"Running in live trading mode with {BROKER}...")
            live_trading()

    if __name__ == '__main__':
        main()

except ImportError as e:
    print(f"Import error: {e}")
    print("Please install required packages: pip install -r requirements.txt")
    remove_lock()
    sys.exit(1)
except Exception as e:
    print(f"Unexpected error: {e}")
    remove_lock()
    sys.exit(1) 